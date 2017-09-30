# -*- coding: utf-8 -*-

from rpc import helloworld_pb2
from rpc import helloworld_pb2_grpc
import grpc
from concurrent import futures
import time


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    while True:
        run()
