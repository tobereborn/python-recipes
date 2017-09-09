# -*- coding: utf-8 -*-
import asyncio
import threading


async def hello():
    print('Hello World! ({0})'.format(threading.current_thread()))
    await asyncio.sleep(10)
    print('Hello again! ({0})'.format(threading.current_thread()))


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([hello(), hello()]))
    loop.close()


if __name__ == '__main__':
    main()
