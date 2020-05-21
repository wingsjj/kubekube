import pymysql
import tasks.task
import datetime


class Db:
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "root")
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        print("Database version : %s " % data)

    def __del__(self):
        self.db.close()

    def add_task(self, user_id, runner, file):
        # SQL 插入语句
        sql = """INSERT INTO kubekube.task(user_id, runner, file, date)
        VALUES (%s, %s, %s, %s)"""
        try:
            # 执行sql语句
            self.cursor.execute(
                sql,
                args=(user_id, runner, file, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            # 提交到数据库执行
            self.db.commit()
        except ValueError as e:
            print(e)
            # 如果发生错误则回滚
            self.db.rollback()

    def add_log(self, task_id, log):
        sql = """insert into kubekube.log(task_id, content)
        values (%s, %s)"""
        try:
            self.cursor.execute(
                sql,
                args=(task_id, log))
            self.db.commit()
        except ValueError as e:
            print(e)
            self.db.rollback()

