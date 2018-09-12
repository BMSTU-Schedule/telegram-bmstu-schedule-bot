#!/usr/local/bin/python3/
import bmstu_schedule
from config.config import access_token
from datetime import datetime
from logger.logger import logger
import os.path
import re
import telebot

bot = telebot.TeleBot(access_token)
reg = re.compile("^[а-яА-Я]{1,4}\d{0,2}\-\d{0,2}[а-яА-Я]?$")
path_to_vault = '/Users/lee/Documents/GitHub/telegram-bmstu-schedule-bot/vault/'
dt = datetime.strptime('2018-09-03', '%Y-%m-%d')

@bot.message_handler(commands=["start"])
def start(message):
    logger(message)
    bot.send_message(message.chat.id, text="Привет, {} {}!".format(message.chat.first_name, message.chat.last_name))



def group_validator(group_id):
    if reg.match(group_id) != None:
        return True
    else:
        return False

def file_exist(file_name):
    return os.path.isfile("{}Расписание {}Б.ics".format(path_to_vault,file_name))



@bot.message_handler(content_types=["text"])
def any_messages(message):
    logger(message)

    if group_validator(message.text):
        if file_exist(message.text):
            file_to_send = open("{}Расписание {}Б.ics".format(path_to_vault,message.text), 'rb')
            bot.send_document(message.chat.id, file_to_send)
        else:
            bmstu_schedule.run(message.text, dt, path_to_vault)
            if file_exist(message.text):
                file_to_send = open("{}Расписание {}.ics".format(path_to_vault,message.text), 'rb')
            else:
                bot.send_message(message.chat.id, text="Не получилось!!!")
    else:
        bot.send_message(message.chat.id, text="Чёт я ничего не нашел для группы '{}'. Если проблема и правда во мне, то напиши @lee_daniil".format(message.text))

    
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=30)
    except Exception as ex:
        pass