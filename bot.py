#!/usr/local/bin/python3/
from config.config import access_token
import datetime
import telebot

bot = telebot.TeleBot(access_token)

@bot.message_handler(commands=["start"])
def greeting(message):
    bot.send_message(message.chat.id, text="Привет, {}!".format(message.chat.first_name))


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=30)
    except Exception as ex:
        # logger написать
        pass
