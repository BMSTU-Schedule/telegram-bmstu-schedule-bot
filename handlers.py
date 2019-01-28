'''
Custom handlers file
'''

import bmstu_schedule
from bot import BOT
from config import CONFIG, SCHEDULE_ICS, SCHEDULE_PNG, DT, GC_REG_MATCHER
from logger.logger import logger
from utils import file_exist

@BOT.message_handler(commands=['start'])
def start(message):
    logger(message)
    BOT.send_message(message.chat.id, text=(
        'Привет!\nЯ помогу тебе получить твоё расписание '
        'в формате,\nудобном для встраивания в любые календари,'
        '\nнапример, Google Calendar или macOS Calendar, и еще '
        '\nкучу других.\nВ какой группе учишься?'))

@BOT.message_handler(content_types=['text'])
def any_messages(message):
    logger(message)
    ics_to_send = ''
    png_to_send = ''

    if not GC_REG_MATCHER.match(message.text):
        BOT.send_message(message.chat.id, text='Мне нужен номер группы, чтобы дать тебе расписание. Например, иу6-54б')
        return

    message.text = message.text.upper()
    BOT.send_message(message.chat.id, text='Уже ищу расписание для группы {}'.format(message.text))

    if file_exist(SCHEDULE_ICS.format(CONFIG['vault'], message.text)):
        ics_to_send = open(SCHEDULE_ICS.format(CONFIG['vault'], message.text), 'rb')
        if file_exist(SCHEDULE_PNG.format(CONFIG['vault'], message.text)):
            png_to_send = open(SCHEDULE_PNG.format(CONFIG['vault'], message.text), 'rb')
    else:
        try:
            bmstu_schedule.run(message.text, DT, CONFIG['vault'])
        except SystemExit:
            BOT.send_message(message.chat.id, text=(
                    'Чёт я ничего не нашел для группы {}. '
                    'Если проблема и правда во мне, и твоё расписание есть на students.bmstu.ru, '
                    'то напиши @lee_daniil или @gabolaev'.format(message.text)))
            return

        if file_exist(SCHEDULE_ICS.format(CONFIG['vault'], message.text)):
            ics_to_send = open(SCHEDULE_ICS.format(CONFIG['vault'], message.text), 'rb')
            if file_exist(SCHEDULE_PNG.format(CONFIG['vault'], message.text)):
                png_to_send = open(SCHEDULE_PNG.format(CONFIG['vault'], message.text), 'rb')
        elif message.text[len(message.text)-1].isnumeric():
            BOT.send_message(message.chat.id, text=(
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
    else:
        BOT.send_message(message.chat.id, text='Мне нужен номер группы, чтобы дать тебе расписание. Например, иу6-54б')

