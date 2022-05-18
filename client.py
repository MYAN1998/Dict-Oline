"""
dict 客户端
"""
from socket import *


# TCP服务类
class TcpServer:
    def __init__(self, host="127.0.0.1", port=8888):
        self.__host = host
        self.__port = port
        self.__addr = (self.__host, self.__port)  # 地址以及端口号
        self.sock = self.__create()  # 创建TCP套接字

    def __create(self):  # 创建TCP套接字
        sock = socket()
        sock.connect(self.__addr)
        return sock

    def login(self, username, password):  # 向服务端请求登录
        request = "LOGIN %s %s" % (username, password)
        self.sock.send(request.encode())
        response = self.sock.recv(1024)
        if response == b"OK":
            return True
        else:
            return False

    def register(self, username, password):  # 向服务端请求注册
        # 判断用户名与密码不能有空格
        if " " in username or " " in password:
            print("用户名或密码不能有空格")
            return
        request = "REG %s %s" % (username, password)
        self.sock.send(request.encode())
        response = self.sock.recv(1024)
        if response == b"OK":
            return True
        else:
            return False

    def exit(self):  # 向服务端请求退出
        request = b"EXIT"
        self.sock.send(request)

    def find(self):
        while True:
            word = input("请输入需要查询的单词:")
            if word == "##":  # 输入##退出查询
                break
            request = "FIND %s" % word
            self.sock.send(request.encode())
            response = self.sock.recv(1024 * 1024)
            print("%s:%s" % (word, response.decode()))

    def log(self):
        self.sock.send(b"LOG")
        # 循环接收
        while True:
            data = self.sock.recv(1024 * 1024)
            if data == b"##":
                break
            print(data.decode())


# 视图交互类
class View:
    def __init__(self):
        self.tcp_server = TcpServer()

    def __interface_two(self):  # 界面2
        while True:
            print("""
            ================主界面=============
            ====1.查单词  2.历史记录  3.注销=====
            ==================================
            """)
            num = input("请输入选项:")
            if num == "1":
                self.tcp_server.find()
            elif num == "2":
                self.tcp_server.log()
            elif num == "3":
                print("注销成功")
                # 进入界面1
                break
            else:
                print("输入有误")

    def interface_one(self):  # 界面1
        while True:
            print("""
            ================主界面=============
            ====1.登录  　　2.注册  　3.退出=====
            ==================================
            """)
            num = input("请输入选项:")
            if num == "1":
                username = input("请输入用户名:")
                password = input("请输入密码:")
                # 判断是否登录成功,成功:进入登录界面2,失败:打印提示消息
                if self.tcp_server.login(username, password):
                    print("登陆成功")
                    self.__interface_two()
                else:
                    print("用户名或密码错误")
            elif num == "2":
                username = input("请输入用户名:")
                password = input("请输入密码:")
                if self.tcp_server.register(username, password):
                    print("注册成功")
                    self.__interface_two()
                else:
                    print("用户名已存在")
            elif num == "3":
                self.tcp_server.exit()
                print("谢谢使用")
                break
            else:
                print("输入有误")


if __name__ == '__main__':
    view = View()
    view.interface_one()  # 调用界面1
