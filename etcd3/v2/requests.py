import typing

from etcd3.etcdrpc import rpc_pb2


def range_request(
    key: bytes,
    range_end: typing.Optional[bytes] = None,
    limit: typing.Optional[int] = None,
    revision: typing.Optional[int] = None,
    sort_order: typing.Optional[
        rpc_pb2.RangeRequest.SortOrder.ValueType
    ] = None,
    sort_target: typing.Optional[
        rpc_pb2.RangeRequest.SortTarget.ValueType
    ] = None,
    serializable: typing.Optional[bool] = None,
    keys_only: typing.Optional[bool] = None,
    count_only: typing.Optional[bool] = None,
    min_mod_revision: typing.Optional[int] = None,
    max_mod_revision: typing.Optional[int] = None,
    min_create_revision: typing.Optional[int] = None,
    max_create_revision: typing.Optional[int] = None
) -> rpc_pb2.RangeRequest:
    request = rpc_pb2.RangeRequest()
    request.key = key
    if range_end is not None:
        request.range_end = range_end
    if limit is not None:
        request.limit = limit
    if revision is not None:
        request.revision = revision
    if sort_order is not None:
        request.sort_order = sort_order
    if sort_target is not None:
        request.sort_target = sort_target
    if serializable is not None:
        request.serializable = serializable
    if keys_only is not None:
        request.keys_only = keys_only
    if count_only is not None:
        request.count_only = count_only
    if min_mod_revision is not None:
        request.min_mod_revision = min_mod_revision
    if max_mod_revision is not None:
        request.max_mod_revision = max_mod_revision
    if min_create_revision is not None:
        request.min_create_revision = min_create_revision
    if max_create_revision is not None:
        request.max_create_revision = max_create_revision
    return request


def put_request(
    key: bytes,
    value: bytes,
    lease: typing.Optional[int] = None,
    prev_kv: typing.Optional[bool] = None,
    ignore_value: typing.Optional[bool] = None,
    ignore_lease: typing.Optional[bool] = None
) -> rpc_pb2.PutRequest:
    request = rpc_pb2.PutRequest()
    request.key = key
    request.value = value
    if lease is not None:
        request.lease = lease
    if prev_kv is not None:
        request.prev_kv = prev_kv
    if ignore_value is not None:
        request.ignore_value = ignore_value
    if ignore_lease is not None:
        request.ignore_lease = ignore_lease
    return request


def delete_range_request(
    key: bytes,
    range_end: typing.Optional[bytes] = None,
    prev_kv: typing.Optional[bool] = None
) -> rpc_pb2.DeleteRangeRequest:
    request = rpc_pb2.DeleteRangeRequest()
    request.key = key
    if range_end is not None:
        request.range_end = range_end
    if prev_kv is not None:
        request.prev_kv = prev_kv
    return request


def txn_compare(
    result: rpc_pb2.Compare.CompareResult.ValueType,
    target: rpc_pb2.Compare.CompareTarget.ValueType,
    key: bytes,
    version: typing.Optional[int] = None,
    create_revision: typing.Optional[int] = None,
    mod_revision: typing.Optional[int] = None,
    value: typing.Optional[bytes] = None,
    range_end: typing.Optional[bytes] = None,
) -> rpc_pb2.Compare:
    compare = rpc_pb2.Compare()
    compare.result = result
    compare.target = target
    compare.key = key
    if version is not None:
        compare.version = version
    if create_revision is not None:
        compare.create_revision = create_revision
    if mod_revision is not None:
        compare.mod_revision = mod_revision
    if value is not None:
        compare.value = value
    if range_end is not None:
        compare.range_end = range_end
    return compare


def txn_request(
    compare: typing.Optional[typing.Iterable[rpc_pb2.Compare]] = None,
    success: typing.Optional[typing.Iterable[typing.Union[
        rpc_pb2.RangeRequest,
        rpc_pb2.PutRequest,
        rpc_pb2.DeleteRangeRequest,
        rpc_pb2.TxnRequest
    ]]] = None,
    failure: typing.Optional[typing.Iterable[typing.Union[
        rpc_pb2.RangeRequest,
        rpc_pb2.PutRequest,
        rpc_pb2.DeleteRangeRequest,
        rpc_pb2.TxnRequest
    ]]] = None,
) -> rpc_pb2.TxnRequest:
    def map_request(
        request: typing.Union[
            rpc_pb2.RangeRequest,
            rpc_pb2.PutRequest,
            rpc_pb2.DeleteRangeRequest,
            rpc_pb2.TxnRequest
        ]
    ) -> rpc_pb2.RequestOp:
        request_range = None
        request_put = None
        request_delete_range = None
        request_txn = None
        if isinstance(request, rpc_pb2.RangeRequest):
            request_range = request
        elif isinstance(request, rpc_pb2.PutRequest):
            request_put = request
        elif isinstance(request, rpc_pb2.DeleteRangeRequest):
            request_delete_range = request
        elif isinstance(request, rpc_pb2.TxnRequest):
            request_txn = request
        else:
            raise
        return rpc_pb2.RequestOp(
            request_range=request_range,
            request_put=request_put,
            request_delete_range=request_delete_range,
            request_txn=request_txn
        )

    def map_requests(
        requests: typing.Optional[typing.Iterable[typing.Union[
            rpc_pb2.RangeRequest,
            rpc_pb2.PutRequest,
            rpc_pb2.DeleteRangeRequest,
            rpc_pb2.TxnRequest
        ]]] = None
    ) -> typing.Optional[typing.Iterable[rpc_pb2.RequestOp]]:
        if requests is not None:
            return [
                map_request(request)
                for request in requests
            ]
        return None

    return rpc_pb2.TxnRequest(
        compare=compare,
        success=map_requests(success),
        failure=map_requests(failure)
    )


def watch_create_request(
    key: bytes,
    range_end: typing.Optional[bytes] = None,
    start_revision: typing.Optional[int] = None,
    progress_notify: typing.Optional[bool] = None,
    filters: typing.Optional[
        typing.Iterable[rpc_pb2.WatchCreateRequest.FilterType.ValueType]
    ] = None,
    prev_kv: typing.Optional[bool] = None
) -> rpc_pb2.WatchCreateRequest:
    request = rpc_pb2.WatchCreateRequest()
    request.key = key
    if range_end is not None:
        request.range_end = range_end
    if start_revision is not None:
        request.start_revision = start_revision
    if progress_notify is not None:
        request.progress_notify = progress_notify
    if filters is not None:
        request.filters.extend(filters)
    if prev_kv is not None:
        request.prev_kv = prev_kv
    return request
