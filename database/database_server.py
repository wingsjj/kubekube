from concurrent import futures
import time
import database.mysql

import grpc

from protos import data_manage_pb2, data_manage_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Manager(data_manage_pb2_grpc.ManagerServicer):

    def __init__(self):
        self.db = database.mysql.Db()

    def AddTask(self, request, context):
        print("AddTask({},{},{})".format(request.user_id, request.runner, request.file))
        self.db.add_task(request.user_id, request.runner, request.file)
        return data_manage_pb2.Reply(code=0, message="success")

    def DeleteTask(self, request, context):
        return data_manage_pb2.Reply(code=0, message="success")

    def QueryTask(self, request, context):
        return data_manage_pb2.Reply(code=0, message="success")

    def UpdateTask(self, request, context):
        return data_manage_pb2.Reply(code=0, message="success")

    def AddTaskLog(self, request, context):
        print("AddTaskLog({},{})".format(request.task_id, request.log))
        self.db.add_log(request.task_id, request.log)
        return data_manage_pb2.Reply(code=0, message="success")

    # # 工作函数
    # def SayHello(self, request, context):
    #     print(request)
    #     date_array = datetime.datetime.utcfromtimestamp(request.date)
    #     other_style_time = date_array.strftime("%Y-%m-%d %H:%M:%S")
    #     print(other_style_time)
    #     return hello_pb2.HelloReply(message='Hello, %s!' % request.name, date=other_style_time)


def serve():
    # gRPC 服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_manage_pb2_grpc.add_ManagerServicer_to_server(Manager(), server)
    server.add_insecure_port('127.0.0.1:50051')
    server.start()  # start() 不会阻塞，如果运行时你的代码没有其它的事情可做，你可能需要循环等待。
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
