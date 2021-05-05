import requests
import threading

from modules.network.websocketClient import Websocket
from modules.network.httpRequests import HttpRequests
from message.messageHandler import MessageHandler

message = MessageHandler()
http = HttpRequests()


def start():
    try:
        # 初始化session文件
        http.init_session()
        print('Session init success.')
    except requests.exceptions.ConnectionError as e:
        # 请求失败则重试
        print('Server not found.')
        start()
    else:
        # 连接 websocket 服务
        # 获取session信息
        session = http.get_session()

        websocket = Websocket(session, handler=message.on_message)
        threading.Thread(target=websocket.run_forever).start()


if __name__ == '__main__':
    start()
