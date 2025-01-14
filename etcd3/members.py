import typing

if typing.TYPE_CHECKING:
    import etcd3.client as client


class Member:
    """
    A member of the etcd cluster.

    :ivar id: ID of the member
    :ivar name: human-readable name of the member
    :ivar peer_urls: list of URLs the member exposes to the cluster for
                     communication
    :ivar client_urls: list of URLs the member exposes to clients for
                       communication
    """

    def __init__(
        self,
        id: int,
        name: str,
        peer_urls: typing.Iterable[str],
        client_urls: typing.Iterable[str],
        etcd_client: 'client.MultiEndpointEtcd3Client'
    ):
        self.id = id
        self.name = name
        self.peer_urls = peer_urls
        self.client_urls = client_urls
        self._etcd_client = etcd_client

    def __str__(self) -> str:
        return ('Member {id}: peer urls: {peer_urls}, client '
                'urls: {client_urls}'.format(id=self.id,
                                             peer_urls=self.peer_urls,
                                             client_urls=self.client_urls))

    def remove(self) -> None:
        """Remove this member from the cluster."""
        self._etcd_client.remove_member(self.id)

    def update(self, peer_urls: typing.Iterable[str]) -> None:
        """
        Update the configuration of this member.

        :param peer_urls: new list of peer urls the member will use to
                          communicate with the cluster
        """
        self._etcd_client.update_member(self.id, peer_urls)

    @property
    def active_alarms(self) -> typing.Iterator['client.Alarm']:
        """Get active alarms of the member.

        :returns: Alarms
        """
        return self._etcd_client.list_alarms(member_id=self.id)
