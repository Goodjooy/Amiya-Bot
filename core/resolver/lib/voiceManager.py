import os
import asyncio

from graiax import silkcoder
from core.util.config import config
from core.util.common import make_folder

loop = asyncio.get_event_loop()
mirai_folder = config('miraiFolder')


class VoiceManager:
    def __init__(self):
        pass

    def voice(self, path):
        filename = path.split('/')[-1].split('.')[0] + '.silk'
        folder = f'{mirai_folder}/data/net.mamoe.mirai-api-http/voices'
        target = f'{folder}/{filename}'

        if not os.path.exists(target):
            make_folder(folder)
            loop.run_until_complete(self.silk_encode(path, target))

        return filename

    @staticmethod
    async def silk_encode(path, res):
        return await silkcoder.encode(path, res, rate=100000)
