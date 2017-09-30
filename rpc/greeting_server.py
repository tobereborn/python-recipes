# -*- coding: utf-8 -*-

from rpc import helloworld_pb2
from rpc import helloworld_pb2_grpc
import grpc
from concurrent import futures
import time

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, {}'.format(request.name))

    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello again, {}'.format(request.name))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    # try:
    #     while True:
    #         time.sleep(_ONE_DAY_IN_SECONDS)
    # except KeyboardInterrupt:
    #     server.stop(0)


if __name__ == '__main__':
    serve()
