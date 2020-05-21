import subprocess
from io import StringIO


class Task:
    def __init__(self, task_id, user_id, runner='python', file=''):
        self.task_id = task_id
        self.user_id = user_id
        self.runner = runner
        self.file = file
        self.io = StringIO()
        self.subprocess = subprocess.Popen(
            [self.runner, self.file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def get_all_output(self) -> str:
        return self.subprocess.stdout.read().decode('utf8')

    def get_output(self) -> str:
        while self.subprocess.poll() is None:
            line = self.subprocess.stdout.readline()
            line = line.strip()
            if line:
                yield line.decode('utf-8')
