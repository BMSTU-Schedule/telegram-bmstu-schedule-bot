#!/usr/local/bin/python3/
from config.config import access_token
import datetime
from logger.logger import logger
import telebot

bot = telebot.TeleBot(access_token)

@bot.message_handler(commands=["start"])
def start(message):
    logger(message)
    bot.send_message(message.chat.id, text="Привет, {} {}!".format(message.chat.first_name, message.chat.last_name))


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=30)
    except Exception as ex:
        pass
