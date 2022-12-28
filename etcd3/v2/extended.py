import typing

from etcd3.etcdrpc import kv_pb2
from etcd3.etcdrpc import rpc_pb2
from etcd3.v2 import client as etcd3_client
from etcd3.v2 import requests
from etcd3.v2 import watch as etcd3_watch

KVKey = typing.Union[bytes, str, int]
KVValue = typing.Union[bytes, str, int]


class KVMetadata:
    def __init__(
        self,
        key_value: kv_pb2.KeyValue,
        header: rpc_pb2.ResponseHeader
    ):
        self.key = key_value.key
        self.create_revision = key_value.create_revision
        self.mod_revision = key_value.mod_revision
        self.version = key_value.version
        self.lease_id = key_value.lease
        self.response_header = header


def prefix_range_end(prefix: bytes) -> bytes:
    """Create a bytestring that can be used as a range_end for a prefix."""
    s = bytearray(prefix)
    for i in reversed(range(len(s))):
        if s[i] < 0xff:
            s[i] = s[i] + 1
            break
    return bytes(s)


def to_bytes(maybe_bytestring: KVKey) -> bytes:
    """
    Encode string to bytes.

    Convenience function to do a simple encode('utf-8') if the input is not
    already bytes. Returns the data unmodified if the input is bytes.
    """
    if isinstance(maybe_bytestring, bytes):
        return maybe_bytestring
    elif isinstance(maybe_bytestring, int):
        return str(maybe_bytestring).encode('utf-8')
    else:
        return maybe_bytestring.encode('utf-8')


def map_one(
    response: rpc_pb2.RangeResponse
) -> typing.Tuple[typing.Optional[bytes], typing.Optional[KVMetadata]]:
    if response.count < 1:
        return None, None
    else:
        kv = response.kvs.pop()
        return kv.value, KVMetadata(kv, response.header)


def map_multiple(
    response: rpc_pb2.RangeResponse
) -> typing.Iterator[typing.Tuple[bytes, KVMetadata]]:
    return (
        (kv.value, KVMetadata(kv, response.header))
        for kv in response.kvs
    )


def map_one_watch_event(
    response: rpc_pb2.WatchResponse
) -> kv_pb2.Event:
    return response.events[0]


def map_multiple_watch_events(
    response: typing.Tuple[
        typing.Iterator[rpc_pb2.WatchResponse],
        typing.Callable[[], None]
    ]
) -> typing.Tuple[
    typing.Iterator[kv_pb2.Event],
    typing.Callable[[], None]
]:
    responses, cancel = response
    return (
        (
            event
            for response in responses
            for event in response.events
        ),
        cancel
    )


SortOrder = typing.Literal['ascend', 'descend']
SORT_ORDERS: typing.Dict[
    typing.Optional[SortOrder],
    rpc_pb2.RangeRequest.SortOrder.ValueType
] = {
    None: rpc_pb2.RangeRequest.NONE,
    'ascend': rpc_pb2.RangeRequest.ASCEND,
    'descend': rpc_pb2.RangeRequest.DESCEND,
}
SortTarget = typing.Literal[
    'key', 'version', 'create', 'mod', 'value'
]
SORT_TARGETS: typing.Dict[
    typing.Optional[SortTarget],
    rpc_pb2.RangeRequest.SortTarget.ValueType
] = {
    None: rpc_pb2.RangeRequest.KEY,
    'key': rpc_pb2.RangeRequest.KEY,
    'version': rpc_pb2.RangeRequest.VERSION,
    'create': rpc_pb2.RangeRequest.CREATE,
    'mod': rpc_pb2.RangeRequest.MOD,
    'value': rpc_pb2.RangeRequest.VALUE,
}


class ExtendedClient:
    def __init__(
        self,
        client: etcd3_client.Client,
        watch: etcd3_watch.Watch
    ):
        self._client = client
        self._watch = watch

    def get_response(
        self,
        key: KVKey,
        **kwargs: typing.Any
    ) -> rpc_pb2.RangeResponse:
        return self._client.range(
            request=requests.range_request(
                key=to_bytes(key),
                **kwargs
            )
        )

    def get(
        self,
        key: KVKey,
        **kwargs: typing.Any
    ) -> typing.Tuple[typing.Optional[bytes], typing.Optional[KVMetadata]]:
        return map_one(
            response=self.get_response(
                key=key,
                **kwargs
            )
        )

    def get_prefix_response(
        self,
        key_prefix: KVKey,
        **kwargs: typing.Any
    ) -> rpc_pb2.RangeResponse:
        key_prefix_bytes = to_bytes(key_prefix)
        return self._client.range(
            request=requests.range_request(
                key=key_prefix_bytes,
                range_end=prefix_range_end(key_prefix_bytes),
                **kwargs
            )
        )

    def get_prefix(
        self,
        key_prefix: KVKey,
        **kwargs: typing.Any
    ) -> typing.Iterator[typing.Tuple[bytes, KVMetadata]]:
        return map_multiple(
            response=self.get_prefix_response(
                key_prefix=key_prefix,
                **kwargs
            )
        )

    def get_range_response(
        self,
        range_start: KVKey,
        range_end: typing.Optional[KVKey],
        sort_order: typing.Optional[SortOrder] = None,
        sort_target: typing.Literal[SortTarget] = 'key',
        **kwargs: typing.Any
    ) -> rpc_pb2.RangeResponse:
        return self._client.range(
            request=requests.range_request(
                key=to_bytes(range_start),
                range_end=(
                    to_bytes(range_end)
                    if range_end is not None
                    else None
                ),
                sort_order=SORT_ORDERS[sort_order],
                sort_target=SORT_TARGETS[sort_target],
                **kwargs
            )
        )

    def get_range(
        self,
        range_start: KVKey,
        range_end: typing.Optional[KVKey],
        sort_order: typing.Optional[SortOrder] = None,
        sort_target: typing.Literal[SortTarget] = 'key',
        **kwargs: typing.Any
    ) -> typing.Iterator[typing.Tuple[bytes, KVMetadata]]:
        return map_multiple(
            response=self.get_range_response(
                range_start=range_start,
                range_end=range_end,
                sort_order=sort_order,
                sort_target=sort_target,
                **kwargs
            )
        )

    def get_all_response(
        self,
        sort_order: typing.Optional[SortOrder] = None,
        sort_target: typing.Literal[SortTarget] = 'key',
        keys_only: bool = False
    ) -> rpc_pb2.RangeResponse:
        return self._client.range(
            request=requests.range_request(
                key=b'\0',
                range_end=b'\0',
                sort_order=SORT_ORDERS[sort_order],
                sort_target=SORT_TARGETS[sort_target],
                keys_only=keys_only
            )
        )

    def get_all(
        self,
        sort_order: typing.Optional[SortOrder] = None,
        sort_target: typing.Literal[SortTarget] = 'key',
        keys_only: bool = False
    ) -> typing.Iterator[typing.Tuple[bytes, KVMetadata]]:
        return map_multiple(
            response=self.get_all_response(
                sort_order=sort_order,
                sort_target=sort_target,
                keys_only=keys_only
            )
        )

    def put(
        self,
        key: KVKey,
        value: KVValue,
        lease: typing.Optional[int] = None,
        prev_kv: bool = False
    ) -> rpc_pb2.PutResponse:
        return self._client.put(
            request=requests.put_request(
                key=to_bytes(key),
                value=to_bytes(value),
                lease=lease,
                prev_kv=prev_kv
            )
        )

    def put_if_not_exists(
        self,
        key: KVKey,
        value: KVValue,
        lease: typing.Optional[int] = None
    ) -> bool:
        key_bytes = to_bytes(key)
        response = self._client.txn(
            request=requests.txn_request(
                compare=[
                    requests.txn_compare(
                        result=rpc_pb2.Compare.CompareResult.EQUAL,
                        target=rpc_pb2.Compare.CompareTarget.CREATE,
                        key=key_bytes,
                        create_revision=0
                    )
                ],
                success=[
                    requests.put_request(
                        key=key_bytes,
                        value=to_bytes(value),
                        lease=lease
                    )
                ]
            )
        )
        return response.succeeded

    def replace(
        self,
        key: KVKey,
        initial_value: KVValue,
        new_value: KVValue
    ) -> bool:
        key_bytes = to_bytes(key)
        response = self._client.txn(
            request=requests.txn_request(
                compare=[
                    requests.txn_compare(
                        result=rpc_pb2.Compare.CompareResult.EQUAL,
                        target=rpc_pb2.Compare.CompareTarget.VALUE,
                        key=key_bytes,
                        value=to_bytes(initial_value)
                    )
                ],
                success=[
                    requests.put_request(
                        key=key_bytes,
                        value=to_bytes(new_value)
                    )
                ]
            )
        )
        return response.succeeded

    def delete(
        self,
        key: KVKey,
        prev_kv: bool = False,
        return_response: bool = False
    ) -> typing.Union[bool, rpc_pb2.DeleteRangeResponse]:
        response = self._client.delete_range(
            request=requests.delete_range_request(
                key=to_bytes(key),
                prev_kv=prev_kv
            )
        )
        if return_response:
            return response
        return response.deleted >= 1

    def delete_prefix(
        self,
        key: KVKey
    ) -> rpc_pb2.DeleteRangeResponse:
        key_bytes = to_bytes(key)
        return self._client.delete_range(
            request=requests.delete_range_request(
                key=key_bytes,
                range_end=prefix_range_end(key_bytes)
            )
        )

    def watch_response(
        self,
        key: KVKey,
        timeout: typing.Optional[float] = None,
        **kwargs: typing.Any
    ) -> typing.Tuple[
        typing.Iterator[rpc_pb2.WatchResponse],
        typing.Callable[[], None]
    ]:
        request = etcd3_watch.watch_create_request(
            key=to_bytes(key),
            **kwargs
        )
        return self._watch.create_iterator(
            request=request,
            timeout=timeout
        )

    def watch(
        self,
        key: KVKey,
        **kwargs: typing.Any
    ) -> typing.Tuple[
        typing.Iterator[kv_pb2.Event],
        typing.Callable[[], None]
    ]:
        return map_multiple_watch_events(
            response=self.watch_response(
                key=key,
                **kwargs
            )
        )

    def watch_prefix_response(
        self,
        key_prefix: KVKey,
        **kwargs: typing.Any
    ) -> typing.Tuple[
        typing.Iterator[rpc_pb2.WatchResponse],
        typing.Callable[[], None]
    ]:
        return self.watch_response(
            key=key_prefix,
            range_end=prefix_range_end(to_bytes(key_prefix)),
            **kwargs
        )

    def watch_prefix(
        self,
        key_prefix: KVKey,
        **kwargs: typing.Any
    ) -> typing.Tuple[
        typing.Iterator[kv_pb2.Event],
        typing.Callable[[], None]
    ]:
        return map_multiple_watch_events(
            response=self.watch_prefix_response(
                key=key_prefix,
                **kwargs
            )
        )

    def watch_once_response(
        self,
        key: KVKey,
        timeout: typing.Optional[float] = None,
        **kwargs: typing.Any
    ) -> rpc_pb2.WatchResponse:
        request = etcd3_watch.watch_create_request(
            key=to_bytes(key),
            **kwargs
        )
        return self._watch.create_once(
            request=request,
            timeout=timeout
        )

    def watch_once(
        self,
        key: KVKey,
        **kwargs: typing.Any
    ) -> kv_pb2.Event:
        return map_one_watch_event(
            self.watch_once_response(
                key=key,
                **kwargs
            )
        )

    def watch_prefix_once_response(
        self,
        key_prefix: KVKey,
        **kwargs: typing.Any
    ) -> rpc_pb2.WatchResponse:
        return self.watch_once_response(
            key=key_prefix,
            range_end=prefix_range_end(to_bytes(key_prefix)),
            **kwargs
        )

    def watch_prefix_once(
        self,
        key_prefix: KVKey,
        **kwargs: typing.Any
    ) -> kv_pb2.Event:
        return map_one_watch_event(
            self.watch_prefix_once_response(
                key_prefix=key_prefix,
                **kwargs
            )
        )
