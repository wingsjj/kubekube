from tasks.task import Task
import queue


class TaskController:

    def __init__(self):
        self.queue = queue.Queue()

    def add_task(self, task: Task):
        self.queue.put(task)

    def now_task(self) -> Task:
        if not self.queue.empty():
            return self.queue.get()
