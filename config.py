# ------------------------------------------------------系统全局设置------------------------------------------------
statucode = ['打卡成功', '系统故障',
             '登录失败', '已经填过',
             '获取失败', '其他错误',
             '验证失败', '未知错误']
detailnum = ['恭喜！今日打卡已经成功',
             '请手动打卡等待系统修复',
             '请检查用户密码是否正确',
             '今日已经填过无需再打卡',
             '无法获取昨日打卡信息！',
             '未知错误, 自行检查打卡',
             '验证码获取或者识别失败',
             '遇到未知错误，打卡失败']
loginUrls = "https://ua.scu.edu.cn/login?service=https%3A%2F%2Fwfw.scu.edu.cn%2Fa_scu%2Fapi%2Fsso%2Fcas-index" \
            "%3Fredirect%3Dhttps%253A%252F%252Fwfw.scu.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex"
postsUrls = "https://wfw.scu.edu.cn/ncov/wap/default/save"
codesUrls = 'https://ua.scu.edu.cn/captcha?captchaId='
PostHeads = {
    'Host': 'wfw.scu.edu.cn',
    'Origin': 'https://wfw.scu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25'
                  ' Safari/537.36 Core/1.70.3754.400 QQBrowser/10.5.4034.400',
    'Accept-Encoding': "gzip, deflate, br",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Type': 'application/x-www-form-urlencoded',
    'Pragma': 'no-cache',
    'Referer': 'https://ua.scu.edu.cn/login?service=https%3A%2F%2Fwfw.scu.edu.cn%2Fa_scu%2Fapi%2Fsso%'
               '2Fcas-index%3Fredirect%3Dhttps%253A%252F%252Fwfw.scu.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
}
global enableLog
enableLog = True
user_list = [
    {
        'username': 'xxxxxxxxxxx',
        'password': 'xxxxxxxx'
    },
    {
        'username': 'xxxxxxxxxxx',
        'password': 'xxxxxxxxx'
    },
    {
        'username': 'xxxxxxxxxxxxx',
        'password': 'xxxxxxx'
    }
]
token_API = "https://api.telegram.org/botxxxxxxxxxxxxxxxxxx/sendMessage"
chat_id = 11111111111111
