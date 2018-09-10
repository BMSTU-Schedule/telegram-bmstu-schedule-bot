import datetime
from config import config
import telebot


def logger(msg):
    if (type(msg) is telebot.types.Message):
        logData = datetime.datetime.now().strftime("%H:%M:%S | %d.%m.%Y")
        log = config.logForm.format(logData, msg.chat.first_name, msg.chat.last_name, msg.chat.username,msg.text)
    else:
        log = msg
    try:
        print(log)
        config.logFile(log)
    except Exception as ex:
        config.logFile(msg=ex)