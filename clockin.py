import re
import time
import json
import signal
import logging
import muggle_ocr
import requests
import datetime
from config import *
from notice import send_tel_bot

sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
logging.captureWarnings(True)


def time_out(interval, callback):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError("Run Func Timeout")

        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)  # interval秒后向进程发送SIGALRM信号
                result = func(*args, **kwargs)
                signal.alarm(0)  # 函数在规定时间执行完后关闭alarm闹钟
                return result
            except TimeoutError or json.decoder.JSONDecodeError as e:
                callback(e)

        return wrapper

    return decorator


# 超时回调函数主体 ------------------------------------------------------------------------------------------------
def timeout_callback(e):
    debugLog('网络错误', '网络错误：连接超时，3秒后将继续')
    time.sleep(3)


# -----------------------------------------------------调试信息输出-----------------------------------------------------
def debugLog(in_head, in_info, in_leve=0):
    global enableLog
    infos = ['信息', '成功', '失败', '警告', '错误', '恐慌', '不幸']
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "[" + in_head + "][" + infos[in_leve] + "]: ", in_info)
    if enableLog:
        with open("./logs/" + time.strftime("%Y-%m-%d", time.localtime()) + ".log", "a") as files:
            files.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                        "[" + in_head + "][" +
                        infos[in_leve] + "]:" +
                        in_info + "\n")


# 执行函数主体 ----------------------------------------------------------------------------------------------------------
@time_out(5, timeout_callback)
def timeouts(cards_user):
    cards_sesi = requests.Session()
    cards_data = usrLogin(cards_user['username'], cards_user['password'], cards_sesi)
    cards_sesi.close()
    return cards_data


# postCard actually post the in_data to the API
def postCard(in_sesi, in_data):
    try:
        cards_temp = eval(in_data[0])
        cards_temp['date'] = time.strftime("%Y%m%d", time.localtime(time.time()))
        cards_info = in_sesi.post(url=postsUrls, headers=PostHeads, data=cards_temp).json()
        if '今天已经填报了' in cards_info['m']:
            return 3
        elif '操作成功' in cards_info['m']:
            return 0
        else:
            return 5
    except requests.exceptions.ConnectionError as e:
        debugLog('网络错误', e, 3)
        return 4
    except ValueError as e:
        debugLog('未知错误', e, 3)
        return 5
    except NameError as e:
        debugLog('未知错误', e, 3)
        return 5
    except BaseException as e:
        debugLog('未知错误', e, 3)
        return 1


# ----------------------------------------------------登录认证函数---------------------------------------------------------
def usrLogin(in_user, in_pass, in_sesi):
    try:
        login_sesi = in_sesi
        login_info = login_sesi.get(url=loginUrls,
                                    headers=PostHeads,
                                    verify=False)
    except requests.exceptions.ConnectionError or BaseException:
        return 1
    # 获取会话验证信息 --------------------------------------------------
    login_even = login_info.text.find('execution')
    login_seid = login_info.text.find('_eventId')
    if login_even > 0 and login_seid > 0:
        try:
            login_exec = login_info.text[login_even + 18:login_seid - 16]
        except ValueError or BaseException:
            return 4
    # 获取验证码code值 --------------------------------------------------
    login_code = login_info.text.find('config.captcha')
    if login_code > 0:
        try:
            login_very = login_info.text[login_code + 47:login_code + 57]
        except ValueError or BaseException:
            login_very = "ERROR"
            debugLog('验证获取', 'RequestGet验证码获取失败!!!!!!!')
            return 6
    else:
        debugLog('验证获取', 'RequestGet验证码获取失败!!!!!!!')
        return 6
    debugLog('验证获取', '已获得本次的验证码ID: ' + login_very)
    # 验证码识别过程 ----------------------------------------------------
    try:
        login_info = login_sesi.get(url=codesUrls + str(login_very),
                                    headers=PostHeads,
                                    verify=False)
        with open('captcha.jpg', 'wb') as file:
            file.write(login_info.content)
        with open(r"captcha.jpg", "rb") as file:
            captcha_bytes = file.read()
            text = sdk.predict(image_bytes=captcha_bytes)
            if len(text) < 6:
                debugLog('验证获取', 'Muggle-OCR验证码获取失败!!!!!!!')
                return 6
            debugLog('验证获取', 'Muggle-OCR识别的验证码是: ' + text.lower())
    except requests.exceptions.ConnectionError as e:
        debugLog('验证获取', e, 2)
        return 6
    except BaseException as e:
        debugLog('验证获取', e, 2)
        return 6
    # 提交登录验证请求 --------------------------------------------------
    login_data = {
        'username': str(in_user),
        'password': str(in_pass),
        'submit': '登录',
        'captcha': text,
        'type': 'username_password',
        '_eventId': 'submit',
        'execution': login_exec
    }
    try:
        login_info = login_sesi.post(url=loginUrls,
                                     data=login_data,
                                     headers=PostHeads,
                                     verify=False)
    except requests.exceptions.ConnectionError or BaseException:
        return 1

    if login_info.text.find('川大疫情防控每日报系统') < 0:
        if login_info.text.find('移动微服务') >= 0:
            return 6
        else:
            return 1
    try:
        login_last = re.findall(r'.*?oldInfo: (.*),.*?', login_info.text)
    except ValueError or BaseException:
        return 4

    if login_last == '':
        return 4

    debugLog('开始打卡', '用户登录成功, 开始执行打卡进程!')
    return postCard(in_sesi, login_last)


# logs all users' tasks
def autoCard():
    debugLog("自动打卡", "-------------------------------")
    debugLog("自动打卡", "开始执行" + datetime.datetime.now().strftime('%Y-%m-%d-%H') + "的打卡任务", 0)
    debugLog("自动打卡", "-------------------------------")

    for cards_user in user_list:
        debugLog("自动打卡", "-------------------------------")
        debugLog('当前选中', '当前选中用户学号: ' + str(cards_user['username']), 0)
        try_times = 10
        while True:
            cards_data = timeouts(cards_user)
            if cards_data in [0, 3]:  # success or already filled
                debugLog('打卡结果', statucode[cards_data] + ',' + detailnum[cards_data], 1)
                break
            if try_times <= 1:
                debugLog('打卡结果', statucode[cards_data] + ',' + detailnum[cards_data])
                debugLog('打卡结果', '此用户全部打卡尝试失败,跳过打卡')
                break
            else:
                debugLog('打卡结果', statucode[cards_data] + ',' + detailnum[cards_data])
                debugLog('打卡结果', '第' + str(11 - try_times) + '次打卡尝试失败，即将重试打卡')
                try_times = try_times - 1

    debugLog("自动打卡", "-------------------------------")
    debugLog("自动打卡", "成功完成" + datetime.datetime.now().strftime('%Y-%m-%d-%H') + "的打卡任务", 0)
    debugLog("自动打卡", "-------------------------------")


# -----------------------------------------------------主要调用入口-------------------------------------------------------
if __name__ == '__main__':
    autoCard()
    send_tel_bot(token_API, chat_id)
