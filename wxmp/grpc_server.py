import grpc
import subprocess
from concurrent import futures
from proto import wxmp_pb2, wxmp_pb2_grpc


SYSTEM_PASSWORD = "jetbot"


class Greeter(wxmp_pb2_grpc.WXMPServicer):

    def ctrl(self, request, context):
        print("restart wxmp")
        cmd = "echo '{}' | sudo -S sudo systemctl restart wxmp".format(SYSTEM_PASSWORD)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output.wait()
        tmp = str(output.stdout.read(), encoding='utf-8')
        print(tmp)
        return wxmp_pb2.ResponseParams()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    wxmp_pb2_grpc.add_WXMPServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()