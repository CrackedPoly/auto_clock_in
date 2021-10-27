import re
import time

import requests


def send_tel_bot(send_url, chat_id):
    with open("./logs/" + time.strftime("%Y-%m-%d", time.localtime()) + ".log", "r") as file:
        words = re.findall("学号: [0-9]{13}|\[成功\].*", file.read())
    msg = "\n".join(words)
    msg = msg + "\n打卡成功人数: " + str(int(len(words) / 2))
    # print(msg)
    requests.post(url=send_url,
                  data={"chat_id": chat_id, "text": msg})
