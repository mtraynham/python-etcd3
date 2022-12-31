import logging
import typing

import grpc

import etcd3.etcdrpc as etcdrpc
import etcd3.events as etcd3_events
import etcd3.exceptions as exceptions
import etcd3.utils as utils
from etcd3.v2 import requests
from etcd3.v2 import watch


_log = logging.getLogger(__name__)


WatchCallbackArg = typing.Union[
    'WatchResponse',
    grpc.RpcError,
    exceptions.RevisionCompactedError
]
WatchCallback = typing.Callable[[WatchCallbackArg], None]


class Watcher:

    def __init__(
        self,
        watchstub: etcdrpc.WatchStub,
        timeout: typing.Optional[typing.Union[int, float]] = None,
        call_credentials: typing.Optional[grpc.CallCredentials] = None,
        metadata: typing.Optional[
            typing.Tuple[typing.Tuple[str, str]]
        ] = None
    ):
        self._watch = watch.Watch(
            watch_stub=watchstub,
            call_credentials=call_credentials,
            timeout=timeout,
        )

    def add_callback(
        self,
        key: typing.Union[bytes, str],
        callback: WatchCallback,
        range_end: typing.Optional[typing.Union[bytes, str]] = None,
        start_revision: typing.Optional[int] = None,
        progress_notify: bool = False,
        filters: typing.Optional[
            typing.Iterable[
                etcdrpc.WatchCreateRequest.FilterType.ValueType
            ]
        ] = None,
        prev_kv: bool = False
    ) -> int:
        request = requests.watch_create_request(
            key=utils.to_bytes(key),
            range_end=utils.to_bytes(range_end) if range_end else None,
            start_revision=start_revision,
            progress_notify=progress_notify,
            filters=filters,
            prev_kv=prev_kv
        )

        def success_callback(
            response: typing.Optional[etcdrpc.WatchResponse]
        ) -> None:
            if response is not None:
                callback(
                    WatchResponse(
                        header=response.header,
                        events=[
                            etcd3_events.new_event(event)
                            for event in response.events
                        ]
                    )
                )

        def error_callback(exception: BaseException) -> None:
            try:
                callback(exception)  # type: ignore
            except Exception:
                pass

        watch_create = self._watch.create(
            request=request,
            callback=success_callback,
            error_callback=error_callback
        )

        return watch_create.watch_id

    def cancel(self, watch_id: int) -> None:
        self._watch.cancel(watch_id)

    def close(self) -> None:
        self._watch.close()


class WatchResponse:

    def __init__(
        self,
        header: etcdrpc.ResponseHeader,
        events: typing.List[etcd3_events.Event]
    ):
        self.header = header
        self.events = events
