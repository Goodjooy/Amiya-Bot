from modules.commonMethods import Reply
import random
from modules.config import get_config

config: dict = get_config()


def repeat(data):
    message = data['text']

    if random.random() < config.get("repeat_probability", 0):
        return Reply(message, at=False)
    else:
        return None
