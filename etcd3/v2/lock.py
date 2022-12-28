import typing
from uuid import uuid4

from etcd3.etcdrpc import rpc_pb2
from etcd3.v2 import client as etcd3_client
from etcd3.v2 import requests


def acquire_request(
    key: bytes,
    uuid: bytes,
    lease: rpc_pb2.LeaseGrantResponse
) -> rpc_pb2.TxnRequest:
    return requests.txn_request(
        compare=[
            requests.txn_compare(
                result=rpc_pb2.Compare.CompareResult.EQUAL,
                target=rpc_pb2.Compare.CompareTarget.CREATE,
                key=key,
                create_revision=0
            )
        ],
        success=[
            requests.put_request(
                key=key,
                value=uuid,
                lease=lease.ID
            )
        ],
        failure=[
            requests.range_request(
                key=key
            )
        ]
    )


def release_request(
    key: bytes,
    uuid: bytes
) -> rpc_pb2.TxnRequest:
    return requests.txn_request(
        compare=[
            requests.txn_compare(
                result=rpc_pb2.Compare.CompareResult.EQUAL,
                target=rpc_pb2.Compare.CompareTarget.VALUE,
                key=key,
                value=uuid
            )
        ],
        success=[
            requests.delete_range_request(
                key=key
            )
        ]
    )


class Lock:
    def __init__(
        self,
        name: str,
        client: etcd3_client.Client,
        ttl: int = 60
    ):
        self._client = client
        self._key = f'/locks/{name}'.encode('utf-8')
        self._uuid = uuid4().bytes
        self._ttl = ttl
        self._lease: typing.Optional[rpc_pb2.LeaseGrantResponse] = None
        self._revision: typing.Optional[int] = None

    def acquire(self) -> bool:
        self._lease = self._client.lease_grant(ttl=self._ttl)
        response = self._client.txn(
            request=acquire_request(
                key=self._key,
                uuid=self._uuid,
                lease=self._lease
            )
        )
        txn_response = response.responses.pop()
        if response.succeeded:
            response_put = txn_response.response_put
            self._revision = response_put.header.revision
        else:
            response_range = txn_response.response_range
            self._revision = response_range.kvs.pop().mod_revision
            self._lease = None
        return response.succeeded

    def is_acquired(self) -> bool:
        response = self._client.range(
            requests.range_request(self._key)
        )
        kv = response.kvs.pop()
        return kv is not None and kv.value == self._uuid

    def refresh(self) -> typing.List[rpc_pb2.LeaseKeepAliveResponse]:
        if self._lease is not None:
            return list(self._client.lease_keep_alive(iter([self._lease.ID])))
        return []

    def release(self) -> bool:
        response = self._client.txn(
            request=release_request(
                key=self._key,
                uuid=self._uuid
            )
        )
        if response.succeeded:
            self._lease = None
        return response.succeeded
