'''
Bot initialization file
'''

import telebot

from bmstu_schedule_bot import configs
from bmstu_schedule_bot import logger

bot = telebot.TeleBot(configs.CONFIG['token'])
logger = logger.Logger(configs.CONFIG['logfile'])
