# auto_clock_in
Clock in automatically in SCU.

## Features
send logs to Telegram bot

## How to use?
`pip install -r requirements.txt` ()

edit `user_list`, `token_API` and `chat_id` in your `config.py`

`python clockin.py` to run your one day task

## Suggestions
`pip install muggle_ocr==1.0.3 -i https://mirrors.aliyun.com/pypi/simple/`

use crontab to create a daily mission: 

`0 8 * * * python3 /home/lighthouse/auto_clock_in/clockin.py`(clock in at 8:00 every day)