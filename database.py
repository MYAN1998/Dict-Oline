"""
dict　数据处理端
"""
import pymysql
import hashlib


class DataHandle:
    def __init__(self):
        self.args = {
            "host": "localhost",  # 本地访问数据库
            "port": 3306,
            "user": "root",  # 根据自己的数据库用户更改
            "password": "123456",  # 输入对应用户的登录密码
            "database": "dict",  # 如果使用其他数据库,自行更改
            "charset": "utf8"
        }
        self.__create()

    # 密码加密函数
    def __change_password(self, password):
        hash = hashlib.sha256()
        hash.update(password.encode())
        return hash.hexdigest()

    def __create(self):
        # 打开数据库和游标
        self.db = pymysql.connect(**self.args)
        self.cur = self.db.cursor()

    def login(self, username, password):
        # 对密码加密
        password = self.__change_password(password)
        # 查找所有用户姓名
        sql = "select name from user where binary name=%s and password=%s;"
        self.cur.execute(sql, [username, password])
        if self.cur.fetchone():  # 如果非空则证明用户名与密码正确
            return True
        return False

    def register(self, username, password):
        # 对密码加密
        password = self.__change_password(password)
        sql = "insert into user (name,password) values (%s,%s);"
        try:  # 尝试将注册信息写入数据库
            self.cur.execute(sql, [username, password])
            # 写操作需要提交
            self.db.commit()
            return True
        except:  # 如果用户名存在则发生异常
            self.db.rollback()
            return False

    def find(self, name, word):
        sql = "select mean from words where word=%s;"
        self.cur.execute(sql, word)
        response = self.cur.fetchone()
        # 如果单词存在,则能够查到对应解释,将解释返回给服务端,并将记录写入数据库
        if response:
            self.__write_log(name, word)
            return response[0]
        # 查不到返回False
        return "NOT FOUND"

    def log(self, name):
        sql = "select name,word,time from user left join history " \
              "on user.id=history.user_id left join words on " \
              "words.id=history.words_id where name=%s " \
              "order by time desc limit 10; "
        self.cur.execute(sql, name)
        return self.cur.fetchall()

    def __write_log(self, name, word):  # 将记录写入数据库
        # 在words数据表中查找单词对应的ID
        sql = "select id from words where word=%s;"
        self.cur.execute(sql, word)
        word_id = self.cur.fetchone()
        # 在user数据表中查找用户名对应的ID
        sql = "select id from user where name=%s;"
        self.cur.execute(sql, name)
        user_id = self.cur.fetchone()
        # 将查找到的用户ID与单词ID写入数据表history
        sql = "insert into history (user_id,words_id) values (%s,%s);"
        self.cur.execute(sql, [user_id, word_id])
        # 写操作需要提交
        self.db.commit()

    def close(self):  # 关闭
        self.cur.close()
        self.db.close()
