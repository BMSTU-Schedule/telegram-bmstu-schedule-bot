import config
import datetime
import telebot

log_form = "{} | {} {}({}) sent: '{}'"

def log_file(msg):
    with open("logfile.txt", "a") as file:
        file.write(str(msg) + "\n")

def logger(msg):
    if (type(msg) is telebot.types.Message):
        log_data = datetime.datetime.now().strftime("%H:%M:%S | %d.%m.%Y")
        log = log_form.format(log_data, msg.chat.first_name, msg.chat.last_name, msg.chat.username,msg.text)
    else:
        log = msg
    try:
        print(log)
        log_file(log)
    except Exception as ex:
        log_file(msg=ex)