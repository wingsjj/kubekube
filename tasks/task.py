import subprocess
from io import StringIO


class Task:
    def __init__(self, task_id, user_id, runner='python', file=''):
        self.task_id = task_id
        self.user_id = user_id
        self.runner = runner
        self.file = file
        self.subprocess: subprocess.Popen

    def get_all_output(self) -> str:
        return self.subprocess.stdout.read().decode('utf8')

    def get_output(self) -> str:
        while self.subprocess.poll() is None:
            out = self.subprocess.stdout.readline()
            line = out.strip()
            if line:
                yield line.decode('utf-8')

    def run(self):
        self.subprocess = subprocess.Popen(
            [self.runner, self.file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def kill(self):
        self.subprocess.kill()

    def status(self) -> int:
        return self.subprocess.returncode
