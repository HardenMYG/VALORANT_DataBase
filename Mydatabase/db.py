import pymysql
from pymysql import OperationalError, MySQLError


class Database:
    def __init__(self): 
        try:
            self.conn = pymysql.connect(
                host='localhost',
                user='root',
                password='13013035208Gmy',
                database='Valorant',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()

        except OperationalError as err:
            print(f"连接失败: {err}")
            exit(1)

    def verify_admin(self, username, password):
        self.cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
        result = self.cursor.fetchone()
        return result is not None

    def verify_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = self.cursor.fetchone()
        return result is not None

    def register_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            self.conn.commit()
        except pymysql.Error as err:
            if err.args[0] == 1062:  # 唯一键冲突
                raise ValueError("用户名已存在")
            else:
                raise err

    def start_transaction(self):
        self.conn.begin()

    def commit_transaction(self):
        if self.conn.open:
            self.conn.commit()

    def rollback_transaction(self):
        if self.conn.open:
            self.conn.rollback()
