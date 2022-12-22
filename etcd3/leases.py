import typing

import etcd3.etcdrpc as etcdrpc

if typing.TYPE_CHECKING:
    import etcd3.client as client


class Lease:
    """
    A lease.

    :ivar id: ID of the lease
    :ivar ttl: time to live for this lease
    """

    def __init__(
        self,
        lease_id: int,
        ttl: int,
        etcd_client: 'client.MultiEndpointEtcd3Client'
    ):
        self.id = lease_id
        self.ttl = ttl

        self.etcd_client = etcd_client

    def _get_lease_info(self) -> etcdrpc.LeaseTimeToLiveResponse:
        return self.etcd_client.get_lease_info(self.id)

    def revoke(self) -> None:
        """Revoke this lease."""
        self.etcd_client.revoke_lease(self.id)

    def refresh(self) -> typing.List[etcdrpc.LeaseKeepAliveResponse]:
        """Refresh the time to live for this lease."""
        return list(self.etcd_client.refresh_lease(self.id))

    @property
    def remaining_ttl(self) -> int:
        return self._get_lease_info().TTL

    @property
    def granted_ttl(self) -> int:
        return self._get_lease_info().grantedTTL

    @property
    def keys(self) -> typing.Iterable[bytes]:
        return self._get_lease_info().keys
