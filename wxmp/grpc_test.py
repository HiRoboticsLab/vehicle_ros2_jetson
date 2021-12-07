from proto import wxmp_pb2

request = wxmp_pb2.RequestRestart()
print(request.SerializeToString())
# # 反序列化
# request.ParseFromString()