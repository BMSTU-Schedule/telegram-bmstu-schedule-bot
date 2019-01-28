'''
Logger file
'''

import datetime
import telebot

message_log_fmt = "{} - {} {}[{}] sent: '{}'"
common_log_fmt = "{} - [INFO]: {}"

def log_file(msg):
    with open("logfile.txt", "a") as file:
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