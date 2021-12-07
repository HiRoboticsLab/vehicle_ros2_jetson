# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import wxmp_pb2 as wxmp__pb2


class WXMPStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ctrl = channel.unary_unary(
                '/WXMP/ctrl',
                request_serializer=wxmp__pb2.RequestParams.SerializeToString,
                response_deserializer=wxmp__pb2.ResponseParams.FromString,
                )


class WXMPServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ctrl(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WXMPServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ctrl': grpc.unary_unary_rpc_method_handler(
                    servicer.ctrl,
                    request_deserializer=wxmp__pb2.RequestParams.FromString,
                    response_serializer=wxmp__pb2.ResponseParams.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'WXMP', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WXMP(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ctrl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WXMP/ctrl',
            wxmp__pb2.RequestParams.SerializeToString,
            wxmp__pb2.ResponseParams.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)