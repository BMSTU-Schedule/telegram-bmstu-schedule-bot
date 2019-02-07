'''
Logger file
'''

import datetime
import telebot
import os

from config import CONFIG

message_log_fmt = "{} - [MESSAGE]{} {}[{}] sent: '{}'"
common_log_fmt = "{} - [INFO]: {}"

log_file_path = CONFIG["logfile"]
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

def log_file(msg):
    with open(log_file_path, "a") as file:
        file.write(str(msg) + "\n")

def logger(msg):
    log_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    if (type(msg) is telebot.types.Message):
        log = message_log_fmt.format(log_date, msg.chat.first_name, msg.chat.last_name, msg.chat.username,msg.text)
    else:
        log = common_log_fmt.format(log_date, str(msg))
    try:
        print(log)
        log_file(log)
    except Exception as ex:
        log_file(msg=ex)