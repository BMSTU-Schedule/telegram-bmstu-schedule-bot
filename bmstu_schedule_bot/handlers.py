import bmstu_schedule
import json
import logging
import os
import random


import replies


from group import Group
from utils import is_file_exists, get_sem_start_date, get_available_types, make_path


log = logging.getLogger("tgbot")


def register_handlers(bot, config):


    @bot.message_handler(commands=['start'])
    def start(message):
        log.info(message)

        bot.send_message(message.chat.id, text=replies.START)


    @bot.message_handler(regexp='([вВ]рач|клиник|[дД]окто|[тТ]ерапе|[бБ]оле[юл])')
    def doctors(message):
        log.info(message)

        path_to_doctors = make_path(config['VAULT_PATH'], "doctors.jpeg")

        if is_file_exists(path_to_doctors):

            with open(path_to_doctors, 'rb') as file:
                bot.send_photo(message.chat.id, file)
                bot.send_message(message.chat.id, text=replies.DOCTORS[0])
        else:
            bot.send_message(message.chat.id, text=replies.DOCTORS[1])


    @bot.message_handler(regexp='(афк|валеологи)')
    def afk(message):
        log.info(message)

        path_to_afk = make_path(config['VAULT_PATH'], "afk.jpg")

        if is_file_exists(path_to_afk):

            with open(path_to_afk, 'rb') as file:
                bot.send_photo(message.chat.id, file)
        else:
            bot.send_message(message.chat.id, text=replies.AFK)
        


def register_custom_handlers(bot, config):


    def get_func_for_handler(bot, value):
        def func(message):
            log.info(message)
            bot.send_message(message.chat.id, text=random.SystemRandom().choice(value))
    
        return func


    with open(config['DIALOGUE_CFG_PATH'], 'r') as file:
        answers = json.loads(file.read())

    for key, value in answers.items():
        new_func = get_func_for_handler(bot, value)
        bot.message_handler(regexp=key)(new_func)



def register_group_parser_handler(bot, config):


    @bot.message_handler(content_types=['text'])
    def any(message):
        log.info(message)

        group = Group.parse_group(message.text)
        if group is None:
            bot.send_message(message.chat.id, text=replies.WRONG_GROUP)
            return

        bot.send_message(message.chat.id, text='Уже ищу твое расписание...')

        path_to_ics = make_path(config['VAULT_PATH'], group.get(), '.ics')

        if not is_file_exists(path_to_ics):
            if not download_schedule(
                    group=group, 
                    api_url=config['BMSTU_SCHEDULE_API'], 
                    path=config['VAULT_PATH']):

                bot.send_message(chat_id, text=replies.GROUP_NOT_FOUND.format(group.get()))
                return

        if not group.has_type():
            available_types = get_available_types(config['VAULT_PATH'], group.get())

            if len(available_types) == 0:
                bot.send_message(chat_id, text=replies.GROUP_IS_NOT_DEFINED.format(group.get()))
                return

            if len(available_types) == 1:
                group.group_type = available_types[0]
            elif is_file_exists(path_to_ics):
                send_also_available_groups_msg(bot, message.chat.id, group, available_types)
            else:
                send_choose_group_type_error_msg(bot, message.chat.id, group, available_types)
                return

        send_schedule(bot, message.chat.id, group.get(), config['VAULT_PATH'])


def download_schedule(group, api_url, path):
    try:
        sem_start_date = get_sem_start_date(api_url)
        bmstu_schedule.run(group.get(), sem_start_date, path)
        return True
    except SystemExit:
        return False


def send_also_available_groups_msg(bot, chat_id, group, available):
    groups = []
    for item in available:
        if item != group.group_type and item != '':
            groups.append(group.name + item)
    ending = 'а' if len(groups) == 1 else 'ы'

    bot.send_message(chat_id, text=(
        'Скидываю расписание для {}. '
        'Также у меня есть групп{} {}'.format(
            group, ending, ', '.join(groups))))


def send_choose_group_type_error_msg(bot, chat_id, group, available):
    for item in available:
        item = group.name + item

    bot.send_message(chat_id, text=(
        'Уточни, пожалуйста, какую из этих групп '
        'ты имеешь в виду: {}?'.format(', '.join(available))))


def send_schedule(bot, chat_id, group, path):
    with open(make_path(path, group, '.ics'), 'rb') as ics:
        bot.send_document(chat_id, ics)

        try:
            with open(make_path(path, group, '.png'), 'rb') as png:
                bot.send_photo(chat_id, png)
        except FileNotFoundError as ex:
            log.error(ex)

        bot.send_message(chat_id, text='Тадам!')
