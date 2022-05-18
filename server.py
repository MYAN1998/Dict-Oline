"""
dict 服务端
"""
import sys
from socket import *
from time import sleep
# database.py与server.py在同一级目录下,即使报错,也没关系
from database import DataHandle
from multiprocessing import Process


# 处理具体逻辑类
class Handle:
    def __init__(self, connfd: socket):
        self.connfd = connfd
        self.data_handle = DataHandle()
        self.name = ""

    def __login(self, username, password):  # 登录处理函数
        # 传递用户名与密码
        if self.data_handle.login(username, password):
            self.name = username  # 登陆成功,设置用户名
            self.connfd.send(b"OK")
        else:
            self.connfd.send(b"FAIL")

    def __register(self, username, password):  # 注册处理函数
        # 传递注册的用户名与密码
        if self.data_handle.register(username, password):
            self.name = username  # 注册成功,设置用户名
            self.connfd.send(b"OK")
        else:
            self.connfd.send(b"FAIL")

    def __find(self, word):  # 查找单词处理函数
        response = self.data_handle.find(self.name, word)
        self.connfd.send(response.encode())

    def __log(self):  # 查看历史记录处理函数
        # log->((name,word,time),()...)
        log = self.data_handle.log(self.name)
        for item in log:
            data = "%s %s %s" % item
            self.connfd.send(data.encode())
            # 防止粘包
            sleep(0.1)
        self.connfd.send(b"##")

    def handle(self):
        while True:
            request = self.connfd.recv(1024).decode()
            # 请求按照空格切割
            temp = request.split(" ")
            # 客户端退出
            if not request or temp[0] == "EXIT":
                break
            elif temp[0] == "LOGIN":  # 登录
                # temp->[LOGIN,username,password]
                self.__login(temp[1], temp[2])
            elif temp[0] == "REG":  # 注册
                # temp->[REG,username,password]
                self.__register(temp[1], temp[2])
            elif temp[0] == "FIND":  # 查单词
                # temp->[FIND,word]
                self.__find(temp[1])
            elif temp[0] == "LOG":  # 查记录
                self.__log()
        # 服务端退出,关闭套接字,关闭数据库连接
        self.data_handle.close()
        self.connfd.close()


# 自定义进程类
class MyProcess(Process):
    def __init__(self, connfd: socket):
        super().__init__()
        self.connfd = connfd
        self.handle = Handle(self.connfd)

    def run(self):
        self.handle.handle()


# TCP服务类
class TcpServer:
    def __init__(self, host="0.0.0.0", port=8888):
        self.__host = host
        self.__port = port
        self.__addr = (self.__host, self.__port)
        self.__sock = self.__create()  # 创建TCP套接字

    def __create(self):
        sock = socket()
        sock.bind(self.__addr)  # 绑定地址以及端口号
        sock.listen(5)  # 设置监听
        return sock

    def start(self):
        while True:
            try:  # 接收来自客户端的请求
                connfd, addr = self.__sock.accept()
                print("connect from", addr)
            except KeyboardInterrupt:  # 服务端异常退出
                self.__sock.close()
                sys.exit("服务结束")
            # 若有客户端连接创建新进程
            process = MyProcess(connfd)
            process.start()


# 程序入口
if __name__ == '__main__':
    tcp_server = TcpServer()
    tcp_server.start()
