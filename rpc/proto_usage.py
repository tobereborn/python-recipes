# -*- coding: utf-8 -*-
from rpc import task_pb2


def main():
    task = task_pb2.Task(content="你好嗎")
    task_buf = task.SerializeToString()
    print(task)
    print(task_buf)
    d_task = task_pb2.Task()
    d_task.ParseFromString(task_buf)
    print(d_task)
    print(d_task.content)


if __name__ == "__main__":
    main()
