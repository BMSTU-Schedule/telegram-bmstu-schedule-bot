'''
Bot main module
'''
import re
import os.path
from datetime import datetime
import urllib3

import bmstu_schedule
import telebot
from config import TOKEN, VAULT_PATH, GROUP_CODE_REGEX
from logger.logger import logger

BOT = telebot.TeleBot(TOKEN)
GC_REG_MATCHER = re.compile(GROUP_CODE_REGEX)
DT = datetime.strptime('2018-09-03', '%Y-%m-%d')
SCHEDULE_ICS = '{}/{}.ics'
SCHEDULE_PNG = '{}/{}.png'


@BOT.message_handler(commands=['start'])
def start(message):
    '''
    handler for user /start command
    '''
    logger(message)
    BOT.send_message(message.chat.id, text=(
        'Привет!\nЯ помогу тебе получить твоё расписание '
        'в формате,\nудобном для встраивания в любые календари,'
        '\nнапример, Google Calendar или macOS Calendar, и еще '
        '\nкучу других.\nВ какой группе учишься?'))


def file_exist(file_path):
    '''
    file existing
    checker
    '''
    return os.path.isfile(file_path)


@BOT.message_handler(content_types=['text'])
def any_messages(message):
    '''
    handler for any
    message containing text
    '''
    logger(message)
    ics_to_send = ''
    png_to_send = ''

    if not GC_REG_MATCHER.match(message.text):
        BOT.send_message(
            message.chat.id, text='Указан неверный формат номера группы.')
        return

    message.text = message.text.upper()
    BOT.send_message(
        message.chat.id,
        text='Пошел искать расписание для группы {}'.format(message.text))

    if file_exist(SCHEDULE_ICS.format(VAULT_PATH, message.text)):
        ics_to_send = open(SCHEDULE_ICS.format(
            VAULT_PATH, message.text), 'rb')
        if file_exist(SCHEDULE_PNG.format(VAULT_PATH, message.text)):
            png_to_send = open(SCHEDULE_PNG.format(
                VAULT_PATH, message.text), 'rb')
    else:
        try:
            bmstu_schedule.run(message.text, DT, VAULT_PATH)
        except SystemExit:
            BOT.send_message(
                message.chat.id, text=(
                    'Чёт я ничего не нашел для группы {}. '
                    'Если проблема и правда во мне, то напиши '
                    '@lee_daniil или @gabolaev'.format(message.text)))
            return

        if file_exist(SCHEDULE_ICS.format(VAULT_PATH, message.text)):
            ics_to_send = open(SCHEDULE_ICS.format(
                VAULT_PATH, message.text), 'rb')
            if file_exist(SCHEDULE_PNG.format(VAULT_PATH, message.text)):
            png_to_send = open(SCHEDULE_PNG.format(
                VAULT_PATH, message.text), 'rb')
        elif message.text[len(message.text)-1].isnumeric():
            BOT.send_message(
                message.chat.id, text=(
                    'Эээ, кажется, кто-то не уточнил тип своей '
                    'группы (Б/М/А). Давай добавим соответствующую  '
                    'букву в конце и попробуем еще раз.  '
                    'Например {}Б'.format(message.text)))
            return

    if ics_to_send:
        BOT.send_document(message.chat.id, ics_to_send)
        if png_to_send:
            BOT.send_photo(message.chat.id, png_to_send)
        BOT.send_message(message.chat.id, text='Тадам!')
        BOT.send_message(
            message.chat.id, text=(
                'Если вдруг будут проблемы при импорте в '
                'календарь, можешь обращаться к @lee_daniil или @gabolaev'))
    else:
        BOT.send_message(
            message.chat.id, text='Указан неверный формат номера группы.')


if __name__ == '__main__':
    try:
        BOT.polling(none_stop=True, timeout=30)
    except urllib3.exceptions.ReadTimeoutError:
        pass
