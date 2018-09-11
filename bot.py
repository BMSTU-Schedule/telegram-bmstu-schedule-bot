#!/usr/local/bin/python3/
from config.config import access_token
from datetime import datetime
from logger.logger import logger
import telebot
import bmstu_schedule
import re

bot = telebot.TeleBot(access_token)
reg = re.compile("^[а-яА-Я]{0,4}\d{0,2}\-\d{0,2}[а-яА-Я]?$")

@bot.message_handler(commands=["start"])
def start(message):
    logger(message)
    bot.send_message(message.chat.id, text="Привет, {} {}!".format(message.chat.first_name, message.chat.last_name))

@bot.message_handler(content_types=["text"])
def any_messages(message):
    logger(message)
    message_text = message.text
    if (reg.match(message_text) != None):
        dt = datetime.strptime('2018-09-03', '%Y-%m-%d')
        bmstu_schedule.run(message_text, dt, "/Users/lee/Documents/GitHub/telegram-bmstu-schedule-bot/vault")
        bot.send_message(message.chat.id, text="Получилось!")
    else:
        bot.send_message(message.chat.id, text="Чёт я ничего не нашел для группы '{}'. Если проблема и правда во мне, то напиши @lee_daniil".format(message_text))


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=30)
    except Exception as ex:
        pass
