import tasks.task_controller
import tasks.task


class TaskCreate:

    def __init__(self):
        self.task_controller = tasks.task_controller.TaskController()

    def create_task(self, user_id: int, filename: str, runner='python'):
        print("开始创建 task ……")
        sub = tasks.task.Task(0, user_id, runner, filename)
        self.task_controller.add_task(sub)
        self.task_controller.run()
