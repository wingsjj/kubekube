from tasks.task import Task
import queue
import threading
from database import database_client


class TaskController:

    def __init__(self):
        self.queue = queue.Queue()
        self.manager = database_client.Manager()
        # self.run()

    def add_task(self, task: Task):
        self.queue.put(task)
        self.manager.AddTask(task.user_id, task.runner, task.file)

    def now_task(self) -> Task:
        if not self.queue.empty():
            return self.queue.get()

    def get_task_count(self) -> int:
        return self.queue.qsize()

    def is_empty(self) -> bool:
        return self.queue.empty()

    def start(self):
        while True:
            # print("test")
            if not self.queue.empty():
                now = self.now_task()
                now.run()
                content = now.get_all_output()
                print(content)
                print("保存训练 log ……")
                self.manager.AddTaskLog(now.user_id, content)

    def run_now(self):
        self.now_task().run()

    def kill_now(self):
        self.now_task().kill()

    def run(self):
        print("开始调度……")
        t = threading.Thread(target=self.start())
        t.start()
