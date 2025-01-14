import typing

import etcd3.events as events
import etcd3.leases as leases
import etcd3.watch as watch


def prefix_range_end(prefix: bytes) -> bytes:
    """Create a bytestring that can be used as a range_end for a prefix."""
    s = bytearray(prefix)
    for i in reversed(range(len(s))):
        if s[i] < 0xff:
            s[i] = s[i] + 1
            break
    return bytes(s)


def to_bytes(maybe_bytestring: typing.Union[bytes, str, int]) -> bytes:
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


def lease_to_id(
    lease: typing.Optional[typing.Union[leases.Lease, int, str]]
) -> int:
    """Figure out if the argument is a Lease object, or the lease ID."""
    lease_id = 0
    if lease:
        if hasattr(lease, 'id'):
            lease_id = lease.id
        else:
            try:
                lease_id = int(lease)
            except TypeError:
                pass
    return lease_id


def response_to_event_iterator(
    response_iterator: typing.Iterator[watch.WatchResponse]
) -> typing.Iterator[events.Event]:
    """Convert a watch response iterator to an event iterator."""
    for response in response_iterator:
        for event in response.events:
            yield event
