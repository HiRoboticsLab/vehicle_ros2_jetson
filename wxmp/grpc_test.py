from proto import wxmp_pb2

request = wxmp_pb2.RequestRestart()
print(request.SerializeToString())
# # εεΊεε
# request.ParseFromString()