import json
import logging
import os
import random


from helpers import download_schedule, send_also_available_groups_msg, send_choose_group_type_error_msg, send_schedule
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


        if group.has_type():
            if not is_file_exists(path_to_ics):
                try:
                    download_schedule(group, config['BMSTU_SCHEDULE_API'], config['VAULT_PATH'])
                except SystemExit:
                    bot.send_message(message.chat.id, text=replies.GROUP_NOT_FOUND.format(group.get()))
                    return
        else:
            available_types = get_available_types(config['VAULT_PATH'], group.get())

            if len(available_types) == 0:
                bot.send_message(message.chat.id, text=replies.GROUP_IS_NOT_DEFINED.format(group.get()))
                return

            if len(available_types) == 1:
                group.group_type = available_types[0]
            else:
                if is_file_exists(path_to_ics):
                    send_also_available_groups_msg(bot, message.chat.id, group, available_types)
                else:
                    send_choose_group_type_error_msg(bot, message.chat.id, group, available_types)
                    return

        send_schedule(bot, message.chat.id, group.get(), config['VAULT_PATH'])
