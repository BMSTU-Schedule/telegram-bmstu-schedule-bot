#!/usr/local/bin/python3/
from config.config import access_token
from datetime import datetime
from logger.logger import logger
import telebot
import bmstu_schedule

bot = telebot.TeleBot(access_token)

@bot.message_handler(commands=["start"])
def start(message):
    logger(message)
    bot.send_message(message.chat.id, text="Привет, {} {}!".format(message.chat.first_name, message.chat.last_name))




@bot.message_handler(content_types=["text"])
def anyMessages(message):
    logger(message)
    bot.send_message(message.chat.id, text="Чёт я ничего не нашел для группы {}. Если проблема и правда во мне, то напиши @lee_daniil".format(message.text))


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=30)
    except Exception as ex:
        pass

# dt = datetime.strptime('2018-09-03', '%Y-%m-%d')
# bmstu_schedule.run("ИУ6-54", dt, "/Users/lee/Documents/GitHub/telegram-bmstu-schedule-bot/vault")