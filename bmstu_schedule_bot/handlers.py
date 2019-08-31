import json
import logging
import os
import random


import bmstu_schedule


from schedule import Group
from utils import is_file_exists, get_sem_start_date


log = logging.getLogger("tgbot")


def register_handlers(bot, config):


    @bot.message_handler(commands=['start'])
    def start(message):
        log.info(message)

        bot.send_message(message.chat.id, text=(
            'Привет!\nЯ помогу тебе получить твоё расписание '
            'в формате,\nудобном для встраивания в любые календари,'
            '\nнапример, Google Calendar или macOS Calendar, и еще '
            '\nкучу других.\nВ какой группе учишься?')
        )


    @bot.message_handler(regexp='([вВ]рач|клиник|[дД]окто|[тТ]ерапе|[бБ]оле[юл])')
    def doctor(message):
        log.info(message)

        path_to_doctors = "{}/{}".format(config['VAULT_PATH'], "doctors.jpeg")

        if is_file_exists(path_to_doctors):

            with open(path_to_doctors, 'rb') as file:
                bot.send_photo(message.chat.id, file)
                bot.send_message(message.chat.id, text='Не болей только(')
        else:
            bot.send_message(message.chat.id, text='Расписания врачей у меня временно нет...')


    @bot.message_handler(regexp='(афк|валеологи)')
    def afk(message):
        log.info(message)

        path_to_afk = "{}/{}".format(config['VAULT_PATH'], "afk.jpg")

        if is_file_exists(path_to_afk):

            with open(path_to_afk, 'rb') as file:
                bot.send_photo(message.chat.id, file)
        else:
            bot.send_message(message.chat.id, text='Расписания афк у меня временно нет...')


    # @bot.message_handler(content_types=['text'])
    # def any_messages(message):
    #     log.info(message)

    #     group = Group.parse_group(message.text)
    #     if group is None:
    #         bot.send_message(message.chat.id, text=(
    #                 'Мне нужен номер группы, чтобы дать тебе расписание, '
    #                 'например, иу6-64. Также ты можешь написать "врачи" или "афк"'))
    #         return

    #     bot.send_message(message.chat.id, text='Уже ищу твое расписание...')

    #     path_to_ics = "{}/{}.ics".format(config['VAULT_PATH'], group.get())

    #     if not is_file_exists(path_to_ics):
    #         if not download_schedule(
    #                 group=group, 
    #                 api_url=config['BMSTU_SCHEDULE_API'], 
    #                 path=config['VAULT_PATH']):
    #             send_not_found_error_msg(message.chat.id, group.get())
    #             return

    #     if not group.has_type():
    #         schedules = schedule.get_available_types(
    #             configs.CONFIG['vault'], group.get())
    #         if len(schedules) == 0:
    #             send_define_group_type_error_msg(message.chat.id, group.get())
    #             return
    #         if len(schedules) == 1:
    #             group.group_type = schedules[0]
    #         elif is_schedule_exists(group):
    #             send_also_available_groups_msg(message.chat.id, group, schedules)
    #         else:
    #             send_choose_group_type_error_msg(message.chat.id, group, schedules)
    #             return

    #     send_schedule(message.chat.id, group.get())


    # def download_schedule(group, api_url, path):
    #     try:
    #         sem_start_date = get_sem_start_date(api_url)
    #         bmstu_schedule.run(group.get(), sem_start_date, path)
    #         return True
    #     except SystemExit:
    #         return False






    # def send_not_found_error_msg(chat_id, group):
    #     bot.send_message(chat_id, text=(
    #             'Чёт я ничего не нашел для группы {}. '
    #             'Если проблема и правда во мне, и твоё расписание есть '
    #             'на students.bmstu.ru/schedule/list, '
    #             'то напиши @lee_daniil, @gabolaev или @ed_asriyan'.format(group)))


    # def send_define_group_type_error_msg(chat_id, group):
    #     bot.send_message(chat_id, text=(
    #             'Эээ, кажется, кто-то не уточнил тип своей '
    #             'группы (Б/М/А). Давай добавим соответствующую  '
    #             'букву в конце и попробуем еще раз.  '
    #             'Например {}Б'.format(group)))


    # def send_also_available_groups_msg(chat_id, group, available):
    #     groups = []
    #     for item in available:
    #         if item != group.group_type and item != '':
    #             groups.append(group.name + item)
    #     ending = 'а' if len(groups) == 1 else 'ы'

    #     bot.send_message(chat_id, text=(
    #         'Скидываю расписание для {}. '
    #         'Также у меня есть групп{} {}'.format(
    #             group, ending, ', '.join(groups))))


    # def send_choose_group_type_error_msg(chat_id, group, available):
    #     for item in available:
    #         item = group.name + item

    #     bot.send_message(chat_id, text=(
    #         'Уточни, пожалуйста, какую из этих групп '
    #         'ты имеешь в виду: {}?'.format(', '.join(available))))


    # def send_schedule(chat_id, group):
    #     with open(
    #         configs.SCHEDULE_ICS.format(configs.CONFIG['vault'], group), 'rb'
    #     ) as ics:
    #         with open(
    #             configs.SCHEDULE_PNG.format(configs.CONFIG['vault'], group), 'rb'
    #         ) as png:
    #             bot.send_document(chat_id, ics)
    #             bot.send_photo(chat_id, png)
    #             bot.send_message(chat_id, text='Тадам!')





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
