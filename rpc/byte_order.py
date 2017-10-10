# -*- coding: utf-8 -*-
import sys
import struct


def main():
    print(sys.byteorder)
    pack=struct.pack('!H', 10)
    print(pack)
    print(struct.unpack('!H', pack))
    print(type(len('hhhhh'.encode('utf-8'))))


if __name__ == "__main__":
    main()
