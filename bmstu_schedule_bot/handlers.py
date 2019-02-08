'''
Custom handlers file
'''

import os

import bmstu_schedule

from bmstu_schedule_bot import BOT
from bmstu_schedule_bot import configs
from bmstu_schedule_bot.logger import logger
from bmstu_schedule_bot import schedule

@BOT.message_handler(commands=['start'])
def start(message):
    logger.log(message)
    BOT.send_message(message.chat.id, text=(
        'Привет!\nЯ помогу тебе получить твоё расписание '
        'в формате,\nудобном для встраивания в любые календари,'
        '\nнапример, Google Calendar или macOS Calendar, и еще '
        '\nкучу других.\nВ какой группе учишься?'))

@BOT.message_handler(regexp='([вВ]рач|клиник|[дД]окто|[тТ]ерапе|[бБ]оле[юл])')
def doctor(message):
	logger.log(message)
    if is_file_exists(configs.CONFIG['doctors']):
        with open(configs.CONFIG['doctors'], 'rb') as jpeg:
            BOT.send_photo(message.chat.id, jpeg)
            BOT.send_message(message.chat.id, text='Не болей только(')
    else:
        BOT.send_message(message.chat.id, text='Расписания врачей у меня временно нет...')

@BOT.message_handler(content_types=['text'])
def any_messages(message):
    logger.log(message)

    group = schedule.parse_group(message.text)
    if group is None:
        BOT.send_message(message.chat.id, text='Мне нужен номер группы, чтобы дать тебе расписание. Например, иу6-64б')
        return

    BOT.send_message(message.chat.id, text='Уже ищу твое расписание...')

    if not is_schedule_exists(group.get()):
        if not download_schedule(message.chat.id, group):
            return

    if not group.has_type():
        schedules = schedule.get_available_types(configs.CONFIG['vault'], group.get())
        if len(schedules) == 0:
            send_define_group_type_error_msg(message.chat.id, group.get())
            return
        if len(schedules) == 1:
            group.group_type = schedules[0]
        elif is_schedule_exists(group):
            send_also_available_groups_msg(message.chat.id, group, schedules)
        else:
            send_choose_group_type_error_msg(message.chat.id, group, schedules)
            return

    send_schedule(message.chat.id, group.get())


def download_schedule(chat_id, group):
    try:
        bmstu_schedule.run(group.get(), configs.SEM_START_DATE, configs.CONFIG['vault'])
        return True
    except SystemExit:
        send_not_found_error_msg(chat_id, group.get())
        return False

def is_file_exists(path):
    return os.path.isfile(path)

def is_schedule_exists(group):
    if is_file_exists(configs.SCHEDULE_ICS.format(configs.CONFIG['vault'], group)):
        return is_file_exists(configs.SCHEDULE_PNG.format(configs.CONFIG['vault'], group))
    return False

def send_not_found_error_msg(chat_id, group):
    BOT.send_message(chat_id, text=(
            'Чёт я ничего не нашел для группы {}. '
            'Если проблема и правда во мне, и твоё расписание есть на students.bmstu.ru/schedule/list, '
            'то напиши @lee_daniil, @gabolaev или @ed_asriyan'.format(group)))

def send_define_group_type_error_msg(chat_id, group):
    BOT.send_message(chat_id, text=(
            'Эээ, кажется, кто-то не уточнил тип своей '
            'группы (Б/М/А). Давай добавим соответствующую  '
            'букву в конце и попробуем еще раз.  '
            'Например {}Б'.format(group)))

def send_also_available_groups_msg(chat_id, group, available):
    groups = []
    for item in available:
        if item != group.group_type and item != '':
            groups.append(group.name + item)
    
    ending = 'а' if len(groups) == 1 else 'ы'
    msg = "Скидываю расписание для {}. Также у меня есть групп{} {}".format(group, ending, ", ".join(groups))
    BOT.send_message(chat_id, text=msg)

def send_choose_group_type_error_msg(chat_id, group, available):
    for item in available:
        item = group.name + item

    msg = "Уточни, пожалуйста, какую из этих групп ты имеешь в виду: {}?".format(", ".join(available))
    BOT.send_message(chat_id, text=msg)

def send_schedule(chat_id, group):
    with open(configs.SCHEDULE_ICS.format(configs.CONFIG['vault'], group), 'rb') as ics:
        with open(configs.SCHEDULE_PNG.format(configs.CONFIG['vault'], group), 'rb') as png:
            BOT.send_document(chat_id, ics)
            BOT.send_photo(chat_id, png)
            BOT.send_message(chat_id, text='Тадам!')