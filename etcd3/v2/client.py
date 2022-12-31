import functools
import typing

import grpc

from etcd3.etcdrpc import rpc_pb2
from etcd3.etcdrpc import rpc_pb2_grpc


class Client:
    def __init__(
        self,
        channel: grpc.Channel,
        timeout: typing.Optional[int] = None,
        call_credentials: typing.Optional[grpc.CallCredentials] = None
    ):
        self._channel = channel
        self._timeout = timeout
        self._call_credentials = call_credentials

    @functools.cached_property
    def _cluster_stub(self) -> rpc_pb2_grpc.ClusterStub:
        return rpc_pb2_grpc.ClusterStub(channel=self._channel)

    @functools.cached_property
    def _kv_stub(self) -> rpc_pb2_grpc.KVStub:
        return rpc_pb2_grpc.KVStub(channel=self._channel)

    @functools.cached_property
    def _lease_stub(self) -> rpc_pb2_grpc.LeaseStub:
        return rpc_pb2_grpc.LeaseStub(channel=self._channel)

    @functools.cached_property
    def _maintenance_stub(self) -> rpc_pb2_grpc.MaintenanceStub:
        return rpc_pb2_grpc.MaintenanceStub(channel=self._channel)

    @functools.cached_property
    def _watch_stub(self) -> rpc_pb2_grpc.WatchStub:
        return rpc_pb2_grpc.WatchStub(channel=self._channel)

    def range(
        self,
        request: rpc_pb2.RangeRequest
    ) -> rpc_pb2.RangeResponse:
        return self._kv_stub.Range(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def put(
        self,
        request: rpc_pb2.PutRequest
    ) -> rpc_pb2.PutResponse:
        return self._kv_stub.Put(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def delete_range(
        self,
        request: rpc_pb2.DeleteRangeRequest
    ) -> rpc_pb2.DeleteRangeResponse:
        return self._kv_stub.DeleteRange(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def txn(self, request: rpc_pb2.TxnRequest) -> rpc_pb2.TxnResponse:
        return self._kv_stub.Txn(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def compact(
        self,
        revision: int,
        physical: bool = False
    ) -> rpc_pb2.CompactionResponse:
        request = rpc_pb2.CompactionRequest(
            revision=revision,
            physical=physical
        )
        return self._kv_stub.Compact(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def lease_grant(
        self,
        ttl: int,
        lease_id: typing.Optional[int] = None
    ) -> rpc_pb2.LeaseGrantResponse:
        request = rpc_pb2.LeaseGrantRequest(TTL=ttl)
        if lease_id is not None:
            request.ID = lease_id
        return self._lease_stub.LeaseGrant(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def lease_time_to_live(
        self,
        lease_id: int,
        keys: bool = True
    ) -> rpc_pb2.LeaseTimeToLiveResponse:
        request = rpc_pb2.LeaseTimeToLiveRequest(
            ID=lease_id,
            keys=keys
        )
        return self._lease_stub.LeaseTimeToLive(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def lease_revoke(
        self,
        lease_id: int
    ) -> rpc_pb2.LeaseRevokeResponse:
        request = rpc_pb2.LeaseRevokeRequest(
            ID=lease_id
        )
        return self._lease_stub.LeaseRevoke(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def lease_keep_alive(
        self,
        lease_ids: typing.Iterator[int]
    ) -> typing.Iterator[rpc_pb2.LeaseKeepAliveResponse]:
        request_iterator = (
            rpc_pb2.LeaseKeepAliveRequest(
                ID=lease_id
            )
            for lease_id in lease_ids
        )
        call_iterator = self._lease_stub.LeaseKeepAlive(
            request_iterator=request_iterator,
            timeout=self._timeout,
            credentials=self._call_credentials
        )
        for response in call_iterator:
            yield response

    def member_list(self) -> rpc_pb2.MemberListResponse:
        request = rpc_pb2.MemberListRequest()
        return self._cluster_stub.MemberList(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def member_add(
        self,
        peer_urls: typing.Iterable[str],
        is_learner: typing.Optional[bool] = None
    ) -> rpc_pb2.MemberAddResponse:
        request = rpc_pb2.MemberAddRequest(
            peerURLs=peer_urls
        )
        if is_learner is not None:
            request.isLearner = is_learner
        return self._cluster_stub.MemberAdd(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def member_update(
        self,
        member_id: int,
        peer_urls: typing.Optional[typing.Iterable[str]] = None
    ) -> rpc_pb2.MemberUpdateResponse:
        request = rpc_pb2.MemberUpdateRequest(
            ID=member_id,
            peerURLs=peer_urls
        )
        return self._cluster_stub.MemberUpdate(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def member_remove(self, member_id: int) -> rpc_pb2.MemberRemoveResponse:
        request = rpc_pb2.MemberRemoveRequest(
            ID=member_id
        )
        return self._cluster_stub.MemberRemove(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def alarm(
        self,
        action: rpc_pb2.AlarmRequest.AlarmAction.ValueType,
        member_id: int,
        alarm: rpc_pb2.AlarmType.ValueType
    ) -> rpc_pb2.AlarmResponse:
        request = rpc_pb2.AlarmRequest(
            action=action,
            memberID=member_id,
            alarm=alarm
        )
        return self._maintenance_stub.Alarm(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def defragment(self) -> rpc_pb2.DefragmentResponse:
        request = rpc_pb2.DefragmentRequest()
        return self._maintenance_stub.Defragment(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def hash(self) -> rpc_pb2.HashResponse:
        request = rpc_pb2.HashRequest()
        return self._maintenance_stub.Hash(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )

    def snapshot(self) -> typing.Iterator[rpc_pb2.SnapshotResponse]:
        request = rpc_pb2.SnapshotRequest()
        call_iterator = self._maintenance_stub.Snapshot(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )
        for response in call_iterator:
            yield response

    def status(self) -> rpc_pb2.StatusResponse:
        request = rpc_pb2.StatusRequest()
        return self._maintenance_stub.Status(
            request=request,
            timeout=self._timeout,
            credentials=self._call_credentials
        )
