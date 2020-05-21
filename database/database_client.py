from __future__ import print_function

import grpc
from protos import data_manage_pb2, data_manage_pb2_grpc


class Manager:
    def __init__(self):
        channel = grpc.insecure_channel('localhost:50051')
        self.stub = data_manage_pb2_grpc.ManagerStub(channel)

    def AddTask(self, user_id, runner, file):
        return self.stub.AddTask(data_manage_pb2.Task(task_id=0, user_id=user_id, runner=runner, file=file))

    def DeleteTask(self, user_id, runner, file):
        pass

    def QueryTask(self, user_id, runner, file):
        pass

    def UpdateTask(self, user_id, runner, file):
        pass

    def AddTaskLog(self, task_id, log):
        return self.stub.AddTaskLog(data_manage_pb2.TaskLog(task_id=task_id, log=log))
