import grpc
from proto import wxmp_pb2, wxmp_pb2_grpc

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = wxmp_pb2_grpc.WXMPStub(channel)
        response: wxmp_pb2.ResponseParams = stub.ctrl(wxmp_pb2.RequestParams())

        print(response)