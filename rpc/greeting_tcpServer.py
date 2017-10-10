# -*- coding: utf-8 -*-
from socketserver import BaseRequestHandler, TCPServer
from threading import Thread
import struct

NWORERS = 16


# message=messageType(1)+taskType(1)+length(4)+content(x)

class GreetingHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            print('Got: {}'.format(msg))
            self.request.send(msg)


def main():
    serv = TCPServer(('', 20000), GreetingHandler)
    for n in range(NWORERS):
        t = Thread(target=serv.serve_forever)
        t.daemon = True
        t.start()
    serv.serve_forever()


if __name__ == "__main__":
    main()
