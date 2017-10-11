# -*- coding: utf-8 -*-
from socket import *
import struct
from rpc import task_pb2

HOST = 'localhost'
PORT = 20000
BUF_SIZE = 1


# message=messageType(1)+taskType(1)+length(4)+content(x)

def send(socket, message_type, task_type, content):
    message_type = struct.pack('!H', message_type)
    task_type = struct.pack('!H', task_type)
    task = task_pb2.Task(content=content).SerializeToString()
    task_len = struct.pack('!I', len(task))
    socket.sendall(message_type)
    socket.sendall(task_type)
    socket.sendall(task_len)
    socket.sendall(task)
    print('Send message_type:{}'.format(message_type))
    print('Send task_type:{}'.format(task_type))
    print('Send task:{}'.format(task))


def recv(socket):
    message_type_buf = socket.recv(2)
    message_type = struct.unpack('!H', message_type_buf)[0]
    task_type_buf = socket.recv(2)
    task_type = struct.unpack('!H', task_type_buf)[0]
    task_len_buf = socket.recv(4)
    task_len = struct.unpack('!I', task_len_buf)[0]
    task_buf = socket.recv(task_len)
    task = task_pb2.Task()
    task.ParseFromString(task_buf)
    print('Recv message_type:{}'.format(message_type))
    print('Recv task_type:{}'.format(task_type))
    print('Recv task content:{}'.format(task.content))


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


# message=messageType(1)+taskType(1)+length(4)+content(x)
def request():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))

    try:
        message_type = 10
        task_type = 20
        content = 'This is the message，你好吗,你好吗,你好吗,你好吗,你好吗'
        send(s, message_type, task_type, content)
        recv(s)

    finally:
        s.close()


if __name__ == "__main__":
    request()
    # time.sleep(2)
