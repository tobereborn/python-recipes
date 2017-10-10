# -*- coding: utf-8 -*-
from socket import *
import time
import struct

HOST = 'localhost'
PORT = 20000
BUF_SIZE = 1


# message=messageType(1)+taskType(1)+length(4)+content(x)

def send(socket, message_type, task_type, content):
    message_type = struct.pack('!H', message_type)
    task_type = struct.pack('!H', task_type)
    content = content.encode('utf-8')
    content_len = struct.pack('!I', len(content))
    socket.sendall(message_type)
    socket.sendall(task_type)
    socket.sendall(content_len)
    socket.sendall(content)
    print('Send message_type:{}'.format(message_type))
    print('Send task_type__byte:{}'.format(task_type))


def recv(socket):
    message_type_buf = socket.recv(2)
    message_type = struct.unpack('!H', message_type_buf)[0]
    task_type_buf = socket.recv(2)
    task_type = struct.unpack('!H', task_type_buf)[0]
    content_len_bytes = socket.recv(4)
    content_len = struct.unpack('!I', content_len_bytes)[0]
    content_bytes = socket.recv(content_len)
    print('Recv message_type:{}'.format(message_type))
    print('Recv task_type:{}'.format(task_type))
    print('Recv content_bytes:{}'.format(content_bytes.decode('utf-8')))


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
