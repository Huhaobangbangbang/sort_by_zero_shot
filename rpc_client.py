# 客户端 RpcClient.py
# -*- coding: utf-8 -*-
import json
import socket
from unittest import result
import os

class TCPClient(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        """链接Server端"""
        self.sock.connect((host, port))

    def send(self, data):
        """将数据发送到Server端"""
        self.sock.send(data)

    def recv(self, length):
        """接受Server端回传的数据"""
        return self.sock.recv(length)


class RPCStub(object):

    def __getattr__(self, function):
        def _func(*args, **kwargs):
            d = {'method_name': function, 'method_args': args, 'method_kwargs': kwargs}
            self.send(json.dumps(d).encode('utf-8'))  # 发送数据
            data = self.recv(1024)  # 接收方法执行后返回的结果
            return data.decode('utf-8')

        setattr(self, function, _func)
        return _func


class RPCClient(TCPClient, RPCStub):
    pass


def input_content():
    huhao = RPCClient()
    huhao.connect('127.0.0.1', 8888)
    # 我们要输入的标签，还有top-k（用户希望展示的个数）
    results = huhao.add('quality', 10)


input_content()
