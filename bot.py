'''
Bot initialization file
'''

import telebot
from config import CONFIG

BOT = telebot.TeleBot(CONFIG['token'])
