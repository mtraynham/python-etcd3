import typing

import grpc

from etcd3.etcdrpc import rpc_pb2
from etcd3.etcdrpc import rpc_pb2_grpc


def create_channel(
    target: str = 'localhost:2379',
    root_certificates_file: typing.Optional[str] = None,
    private_key_file: typing.Optional[str] = None,
    certificate_chain_file: typing.Optional[str] = None,
    options: typing.Optional[
        typing.Sequence[typing.Tuple[str, typing.Any]]
    ] = None
) -> grpc.Channel:
    def read(file: typing.Optional[str]) -> typing.Optional[bytes]:
        if file is not None:
            with open(file, 'rb') as f:
                return f.read()

        return None

    root_certificates = read(root_certificates_file)
    private_key = read(private_key_file)
    certificate_chain = read(certificate_chain_file)

    if root_certificates or (private_key and certificate_chain):
        credentials = grpc.ssl_channel_credentials(
            root_certificates=root_certificates,
            private_key=private_key,
            certificate_chain=certificate_chain
        )
        return grpc.secure_channel(
            target=target,
            credentials=credentials,
            options=options
        )
    else:
        return grpc.insecure_channel(
            target=target,
            options=options
        )


class EtcdTokenCallCredentials(grpc.AuthMetadataPlugin):
    def __init__(self, metadata: grpc.Metadata):
        self._metadata = metadata

    def __call__(
        self,
        context: grpc.AuthMetadataContext,
        callback: grpc.AuthMetadataPluginCallback
    ) -> None:
        callback(self._metadata, None)


def create_call_credentials(
    channel: grpc.Channel,
    name: str,
    password: str,
    timeout: typing.Optional[int] = None
) -> grpc.CallCredentials:
    auth_stub = rpc_pb2_grpc.AuthStub(channel=channel)
    auth_response = auth_stub.Authenticate(
        rpc_pb2.AuthenticateRequest(
            name=name,
            password=password
        ),
        timeout=timeout
    )
    call_metadata = (('token', auth_response.token),)

    return grpc.metadata_call_credentials(
        EtcdTokenCallCredentials(call_metadata)
    )
