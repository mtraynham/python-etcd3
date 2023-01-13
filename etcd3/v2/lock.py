import typing
from uuid import uuid4

from etcd3.v2 import client as etcd3_client
from etcd3.v2 import watch as etcd3_watch
from etcdrpc import rpc_pb2
from v2 import requests


class Lock:
    def __init__(
        self,
        name: str,
        client: etcd3_client.Client,
        watch: etcd3_watch.Watch,
        ttl: int = 60
    ):
        self._client = client
        self._watch = watch
        self._key = f'/locks/{name}'.encode('utf-8')
        self._uuid = uuid4().bytes
        self._ttl = ttl
        self._lease: typing.Optional[rpc_pb2.LeaseGrantResponse] = None
        self._revision: typing.Optional[int] = None

    def _acquire(self) -> typing.Tuple[
        rpc_pb2.LeaseGrantResponse,
        rpc_pb2.TxnResponse
    ]:
        lease = self._client.lease_grant(ttl=self._ttl)
        response = self._client.txn(
            request=requests.txn_request(
                compare=[
                    requests.txn_compare(
                        result=rpc_pb2.Compare.CompareResult.EQUAL,
                        target=rpc_pb2.Compare.CompareTarget.CREATE,
                        key=self._key,
                        create_revision=0
                    )
                ],
                success=[
                    requests.put_request(
                        key=self._key,
                        value=self._uuid,
                        lease=lease.ID
                    )
                ],
                failure=[
                    requests.range_request(
                        key=self._key
                    )
                ]
            )
        )
        return (
            lease,
            response
        )

    def acquire(
        self,
        timeout: typing.Optional[float]
    ) -> bool:
        lease, response = self._acquire()
        if response.succeeded:
            self._lease = lease
        else:
            if timeout:
                self._watch.create_once(
                    request=etcd3_watch.watch_create_request(
                        key=self._key,
                        start_revision=response.responses.response_range.kvs.pop().mod_revision,
                        filters=[rpc_pb2.WatchCreateRequest.FilterType.NOPUT]
                    ),
                    timeout=timeout
                )
                lease, response = self._acquire()
                if response.succeeded:
                    self._lease = lease

        return response.succeeded

    def is_acquired(self) -> bool:
        response = self._client.range(
            requests.range_request(self._key)
        )
        kv = response.kvs.pop()
        return kv is not None and kv.value == self._uuid

    def refresh(self) -> typing.Optional[rpc_pb2.LeaseKeepAliveResponse]:
        if self._lease is not None:
            return next(
                self._client.lease_keep_alive(iter([self._lease.ID]))
            )

        return None

    def release(self) -> bool:
        response = self._client.txn(
            request=requests.txn_request(
                compare=[
                    requests.txn_compare(
                        result=rpc_pb2.Compare.CompareResult.EQUAL,
                        target=rpc_pb2.Compare.CompareTarget.VALUE,
                        key=self._key,
                        value=self._uuid
                    )
                ],
                success=[
                    requests.delete_range_request(
                        key=self._key
                    )
                ]
            )
        )
        if response.succeeded:
            self._lease = None
        return response.succeeded
