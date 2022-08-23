# 服务端 RpcServer.py
# -*- coding: utf-8 -*-
import json
import socket
funs = {}
import json
from tqdm import tqdm
from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer
from tqdm import tqdm
import torch
import os
torch.cuda.is_available()
from zero_shot import sort_get_sentence
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli",device = 1)
def register_function(func):
    """Server端方法注册，Client端只可调用被注册的方法"""
    name = func.__name__
    funs[name] = func

class TCPServer(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None

    def bind_listen(self, port):
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(5)

    def accept_receive_close(self):
        """获取Client端信息"""
        if self.client_socket is None:
            (self.client_socket, address) = self.sock.accept()
        if self.client_socket:
            msg = self.client_socket.recv(1024)
            data = self.on_msg(msg)
            self.client_socket.send(data)  # 回传

class RPCStub(object):

    def __init__(self):
        self.data = None

    def call_method(self, data):
        """解析数据，调用对应的方法变将该方法执行结果返回"""
        if len(data) == 0:
            return json.dumps("something wrong").encode('utf-8')
        self.data = json.loads(data.decode('utf-8'))
        method_name = self.data['method_name']
        method_args = self.data['method_args']
        method_kwargs = self.data['method_kwargs']
        res = funs[method_name](*method_args, **method_kwargs)
        data = res
        return json.dumps(data).encode('utf-8')

class RPCServer(TCPServer, RPCStub):
    def __init__(self):
        TCPServer.__init__(self)
        RPCStub.__init__(self)
        
    
    def loop(self, port):
        # 循环监听 端口
        self.bind_listen(port)
        print('Server listen 8888 ...')
        while True:
            try:
                self.accept_receive_close()
            except Exception:
                self.client_socket.close()
                self.client_socket = None
                continue

    def on_msg(self, data):
        return self.call_method(data)


@register_function
def add(key, topk):
    """输入key和topk"""
    top_k_results = sort_get_sentence(key,classifier,topk)
    
    json_path = '/cloud/cloud_disk/users/huh/nlp/smart_home/script/yiya/cope_dataset/extract_keywords/sort/__pycache__/zero_shot.json'
    out_file = open(json_path, "w")
    json.dump(top_k_results, out_file, indent=6)
    return top_k_results


s = RPCServer()
s.loop(8888)  # 传入要监听的端口
