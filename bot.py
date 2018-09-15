#!/usr/local/bin/python3/
import bmstu_schedule
from config import access_token, path_to_vault
from datetime import datetime
from logger.logger import logger
import os.path
import re
import telebot

bot = telebot.TeleBot(access_token)
reg = re.compile('^[а-яА-Я]{1,4}\d{0,2}\-\d{0,3}[а-яА-Я]?$')
dt = datetime.strptime('2018-09-03', '%Y-%m-%d')
schedule_file = '{}/Расписание {}.ics'

@bot.message_handler(commands=['start'])
def start(message):
    logger(message)
    bot.send_message(message.chat.id, text='Привет!\nЯ помогу тебе получить твоё расписание в формате,\nудобном для встраивания в любые календари,\nнапример, Google Calendar или macOS Calendar, и еще \nкучу других.\nВ какой группе учишься?')

def group_validator(group_id):
    return reg.match(group_id) != None

def file_exist(file_name):
    return os.path.isfile(schedule_file.format(path_to_vault,file_name))

@bot.message_handler(content_types=['text'])
def any_messages(message):
    logger(message)

    if group_validator(message.text):
        message.text = message.text.upper()
        bot.send_message(message.chat.id, text='Пошел искать расписание для группы {}'.format(message.text))

        if file_exist(message.text):
            file_to_send = open(schedule_file.format(path_to_vault, message.text), 'rb')
        else:
            try:
                bmstu_schedule.run(message.text, dt, path_to_vault)
            except SystemExit as ex:
                bot.send_message(message.chat.id, text='Чёт я ничего не нашел для группы {}. Если проблема и правда во мне, то напиши @lee_daniil или @gabolaev'.format(message.text))
                return

            if file_exist(message.text):
                file_to_send = open(schedule_file.format(path_to_vault, message.text), 'rb')
            elif message.text[len(message.text)-1].isnumeric():
                    bot.send_message(message.chat.id, text="Эээ, кажется, кто-то не уточнил тип своей группы (Б/М/А). Давай добавим соответствующую букву в конце и попробуем еще раз. Например {}Б".format(message.text))
                    return
            return
        
        bot.send_document(message.chat.id, file_to_send)
        bot.send_message(message.chat.id, text='Тадам!')
        bot.send_message(message.chat.id, text='Если вдруг будут проблемы при импорте в календарь, можешь обращаться к @lee_daniil или @gabolaev')
    else:
        bot.send_message(message.chat.id, text='Указан неверный формат номера группы.')

    
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=30)
    except Exception as ex:
        pass
        