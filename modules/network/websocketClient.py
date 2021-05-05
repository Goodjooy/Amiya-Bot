import json
import threading

from ws4py.client.threadedclient import WebSocketClient
from modules.automaticAction import run_automatic_action
from modules.config import get_config


class Websocket(WebSocketClient):
    def __init__(self, session, handler=None):
        server = get_config('server')

        host = server['server_ip']
        port = server['server_port']
        super().__init__('ws://%s:%d/all?sessionKey=%s' % (host, port, session))
        self.connect()
        self.handler = handler

    def opened(self):
        # 启动循环事件线程
        run_automatic_action()
        print('websocket connecting success')

    def closed(self, code, reason=None):
        print('websocket lose connection')

    def received_message(self, message):
        """
        接受message的响应函数
        :param message: 二进制或者文本类型的信息
        :return:
        """
        # 将message以json模式解析
        # 信息为二进制->强制转义为Str后解析？
        data = json.loads(str(message))

        if self.handler:
            # 轮询模式响应信息
            # 更换为线程池 + 先进先出队列是否会更好？
            threading.Timer(0, self.handler, args=(data,)).start()
