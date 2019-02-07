'''
Bot initialization file
'''

import telebot
from bmstu_schedule_bot import configs

BOT = telebot.TeleBot(configs.CONFIG['token'])
