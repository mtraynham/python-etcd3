"""A threaded watcher demux implementation.

This setup de-multiplexes a single etcd watch request into multiple
watch response queues.
https://etcd.io/docs/v3.5/learning/api/#watch-streams

Creation of the Watch will spawn the WatchThread and a request
Queue is shared between them.  The queue gets requests from
the user through Watch and the WatchThread reads them off into
the request_iterator for the grpc call.

Watch uses a counter to provide an ID space for client calls
and new integers are provided back to the user for reference
of a watch, similar to that of the server using integer IDs
for response events.

WatchThread will convert back and forth between the server ID
integer and the client ID integer to make the request/response
matching seamless.

A series of Lock holding and Conditional(Lock) waiting is used
to ensure that only a single create request is running at any
given time to match the initial request with the response and
provide the client id -> server id tracking.

'None' is the sentinel object for both the request queue and
response queues.
"""

import dataclasses
import itertools
import queue
import threading
import typing

from etcd3.etcdrpc import rpc_pb2
from etcd3.v2 import client as etcd3_client


class WatchError(Exception):
    def __init__(
        self,
        *args: typing.Any,
        **kwargs: typing.Any
    ):
        super().__init__(*args, **kwargs)


class RevisionCompactedError(WatchError):
    def __init__(
        self,
        compact_revision: int,
        *args: typing.Any,
        **kwargs: typing.Any
    ):
        super(RevisionCompactedError, self).__init__(*args, **kwargs)
        self.compact_revision = compact_revision


class WatchFailedError(WatchError):
    def __init__(
        self,
        reason: str,
        *args: typing.Any,
        **kwargs: typing.Any
    ):
        super(WatchFailedError, self).__init__(*args, **kwargs)
        self.reason = reason


@dataclasses.dataclass
class WatchCreate:
    watch_id: int
    request: rpc_pb2.WatchCreateRequest
    callback: typing.Callable[
        [typing.Optional[rpc_pb2.WatchResponse]],
        None
    ]
    error_callback: typing.Callable[
        [BaseException],
        None
    ]


def noop(
    *_args: typing.Any,
    **_kwargs: typing.Any
) -> None:
    return None


class WatchThread(threading.Thread):
    def __init__(
        self,
        client: etcd3_client.Client,
        request_queue: queue.Queue[
            typing.Optional[
                typing.Union[
                    WatchCreate,
                    rpc_pb2.WatchCancelRequest,
                    rpc_pb2.WatchProgressRequest
                ]
            ]
        ],
        timeout: typing.Optional[float] = None,
        *args: typing.Any,
        **kwargs: typing.Any
    ):
        super().__init__(*args, **kwargs)
        self._client = client
        self._request_queue = request_queue
        self._timeout = timeout
        self._lock = threading.Lock()
        self._lock_condition = threading.Condition(lock=self._lock)
        self._stopping = False
        self._watch_create_ids_to_watch_response_ids: typing.Dict[
            int,
            int
        ] = {}
        self._watch_response_ids_to_watch_creates: typing.Dict[
            int,
            WatchCreate
        ] = {}
        self._current_watch_create: typing.Optional[WatchCreate] = None

    def handle_sentinel_request(
        self
    ) -> typing.Iterator[rpc_pb2.WatchCancelRequest]:
        with self._lock:
            # Wait for any existing lock to finish creating
            while self._current_watch_create:
                self._lock_condition.wait()

            # Put a series of cancel requests
            response_watch_ids = (
                self._watch_response_ids_to_watch_creates.keys()
            )
            for response_watch_id in response_watch_ids:
                yield rpc_pb2.WatchCancelRequest(
                    watch_id=response_watch_id
                )

    def handle_create_request(
        self,
        request: WatchCreate
    ) -> typing.Iterator[rpc_pb2.WatchCreateRequest]:
        with self._lock:
            # Wait for any existing lock to finish creating
            while self._current_watch_create:
                self._lock_condition.wait()
            # Set the current create request
            self._current_watch_create = request
            # Yield back control to the iterator to consume the request
            yield request.request

    def handle_create_response(
        self,
        response: rpc_pb2.WatchResponse
    ) -> None:
        with self._lock:
            # Ensure we have a request in progress
            if self._current_watch_create:
                # Track the request w/ the response
                self._watch_create_ids_to_watch_response_ids[
                    self._current_watch_create.watch_id
                ] = response.watch_id
                self._watch_response_ids_to_watch_creates[
                    response.watch_id
                ] = self._current_watch_create
                # Set the current watch to None to allow new requests
                self._current_watch_create = None
            # Notify the create lock to resume processing
            self._lock_condition.notify_all()

    def handle_cancel_request(
        self,
        request: rpc_pb2.WatchCancelRequest
    ) -> typing.Iterator[rpc_pb2.WatchCancelRequest]:
        # The request will have the watch create id, but
        # it will need to be mapped to the response id
        watch_response_id = self._watch_create_ids_to_watch_response_ids.get(
            request.watch_id
        )
        # Swap the request / response id
        if watch_response_id:
            request.watch_id = watch_response_id
            yield request

    def handle_cancel_response(
        self,
        response: rpc_pb2.WatchResponse
    ) -> None:
        watch_id = response.watch_id
        # Fetch the create request before un-tracking it
        watch_create = self._watch_response_ids_to_watch_creates.get(watch_id)
        # If our watch create exists
        if watch_create:
            # Put a sentinel to it's queue
            watch_create.callback(None)
            # Untrack create id -> response id
            del self._watch_create_ids_to_watch_response_ids[
                watch_create.watch_id
            ]
        # Untrack response id -> create id
        del self._watch_response_ids_to_watch_creates[watch_id]

    def handle_response(
        self,
        response: rpc_pb2.WatchResponse
    ) -> None:
        # Fetch the watch create from the response id
        watch_create = self._watch_response_ids_to_watch_creates.get(
            response.watch_id
        )
        # Simply put the response to the callback if found
        if watch_create is not None:
            response.watch_id = watch_create.watch_id
            watch_create.callback(response)

    def maybe_handle_error_response(
        self,
        response: rpc_pb2.WatchResponse
    ) -> None:
        exception: typing.Optional[BaseException] = None
        if response.compact_revision != 0:
            exception = RevisionCompactedError(
                compact_revision=response.compact_revision
            )
        elif response.cancel_reason:
            exception = WatchFailedError(
                reason=response.cancel_reason
            )

        if exception is not None:
            # Fetch the watch create from the response id
            watch_create = self._watch_response_ids_to_watch_creates.get(
                response.watch_id
            )
            # Pass an error to the error callback
            if watch_create is not None:
                watch_create.error_callback(exception)

    def request_iterator(
        self
    ) -> typing.Iterator[
        typing.Union[
            rpc_pb2.WatchCreateRequest,
            rpc_pb2.WatchCancelRequest,
            rpc_pb2.WatchProgressRequest
        ]
    ]:
        while True:
            request = self._request_queue.get()
            if request is None:
                yield from self.handle_sentinel_request()
                self._request_queue.task_done()
                self._stopping = True
                break
            try:
                if isinstance(request, WatchCreate):
                    yield from self.handle_create_request(request)
                elif isinstance(request, rpc_pb2.WatchCancelRequest):
                    yield from self.handle_cancel_request(request)
                else:
                    yield request
            finally:
                self._request_queue.task_done()

    def response_handler(
        self,
        call_iterator: typing.Iterator[rpc_pb2.WatchResponse]
    ) -> None:
        for response in call_iterator:
            try:
                if response.created:
                    self.handle_create_response(response)

                self.handle_response(response)

                if response.canceled:
                    self.maybe_handle_error_response(response)
            finally:
                if response.canceled:
                    self.handle_cancel_response(response)

                if self._stopping and self._request_queue.empty():
                    break

    def run(self) -> None:
        request_iterator = self.request_iterator()
        call_iterator = self._client.watch(
            request_iterator=request_iterator
        )
        self.response_handler(call_iterator)


class Watch:
    def __init__(
        self,
        client: etcd3_client.Client,
        timeout: typing.Optional[float] = None
    ):
        self._request_queue: queue.Queue[
            typing.Optional[
                typing.Union[
                    WatchCreate,
                    rpc_pb2.WatchCancelRequest,
                    rpc_pb2.WatchProgressRequest
                ]
            ]
        ] = queue.Queue()
        self._id_generator = itertools.count()
        self._thread = WatchThread(
            client=client,
            request_queue=self._request_queue,
            timeout=timeout,
            daemon=True
        )
        self._thread.start()

    def create(
        self,
        request: rpc_pb2.WatchCreateRequest,
        callback: typing.Callable[
            [typing.Optional[rpc_pb2.WatchResponse]],
            None
        ],
        error_callback: typing.Callable[
            [BaseException],
            None
        ] = noop
    ) -> WatchCreate:
        watch_create = WatchCreate(
            watch_id=next(self._id_generator),
            request=request,
            callback=callback,
            error_callback=error_callback
        )
        self._request_queue.put(watch_create)
        return watch_create

    def cancel(self, watch_id: int) -> None:
        request = rpc_pb2.WatchCancelRequest(
            watch_id=watch_id
        )
        self._request_queue.put(request)

    def progress(self) -> None:
        request = rpc_pb2.WatchProgressRequest()
        self._request_queue.put(request)

    def close(self) -> None:
        self._request_queue.put(None)
        self._thread.join()
