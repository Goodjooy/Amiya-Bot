import os
import time
import jieba
import shutil
import datetime
import traceback

jieba.setLogLevel(jieba.logging.INFO)

log_dir = 'log/console'


def info(msg: str, title: str = 'info', alignment: bool = True, log: bool = True):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    front = f'[{date}]' \
            f'[{capitalize(title)}]' \
            f'{" " if msg[0] != "[" else ""}'

    text = capitalize(msg)
    if alignment:
        text = text.replace('\n', '\n' + ' ' * len(front))
    text = front + text

    print(text)

    if log:
        write_in_log(text)


def error(msg: str):
    info(msg, title='error', alignment=False)


def capitalize(text: str):
    return text[0].upper() + text[1:]


def write_in_log(text):
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except FileExistsError:
            pass

    file = f'{log_dir}/%s.log' % time.strftime('%Y%m%d', time.localtime())

    # noinspection PyBroadException
    try:
        with open(file, encoding='utf-8', mode='a+') as log:
            log.write(text + '\n')
    except Exception:
        info(traceback.format_exc(), title='error', log=False)


def clean_log(days, extra: list = None):
    day_ago = datetime.datetime.now() - datetime.timedelta(days=int(days))
    day_ago = int(day_ago.strftime('%Y%m%d'))

    if os.path.exists(log_dir) is False:
        return False

    for root, dirs, files in os.walk(log_dir):
        for item in files:
            filename = int(item.split('.')[0])
            if filename < day_ago:
                os.remove(os.path.join(root, item))

    if extra:
        for item in extra:
            if os.path.exists(item):
                shutil.rmtree(item)