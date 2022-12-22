import typing

import etcd3.etcdrpc.kv_pb2 as kv_pb2


class Event:

    def __init__(self, event: kv_pb2.Event):
        self.key = event.kv.key
        self._event = event

    def __getattr__(self, name: str) -> typing.Any:
        if name.startswith('prev_'):
            return getattr(self._event.prev_kv, name[5:])
        return getattr(self._event.kv, name)

    def __str__(self) -> str:
        return '{type} key={key} value={value}'.format(
            type=self.__class__,
            key=self.key.decode('utf-8'),
            value=self.value.decode('utf-8')
        )


class PutEvent(Event):
    pass


class DeleteEvent(Event):
    pass


def new_event(event: kv_pb2.Event) -> Event:
    """
    Wrap a raw gRPC event in a friendlier containing class.

    This picks the appropriate class from one of PutEvent or DeleteEvent and
    returns a new instance.
    """
    op_name = event.EventType.DESCRIPTOR.values_by_number[event.type].name
    cls: typing.Type[Event]
    if op_name == 'PUT':
        cls = PutEvent
    elif op_name == 'DELETE':
        cls = DeleteEvent
    else:
        raise Exception('Invalid op_name')

    return cls(event)
