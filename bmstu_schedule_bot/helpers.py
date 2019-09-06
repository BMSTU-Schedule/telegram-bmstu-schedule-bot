import bmstu_schedule
import logging


import replies


from utils import get_sem_start_date, make_path


log = logging.getLogger("tgbot")


def download_schedule(group, api_url, path):
    try:
        sem_start_date = get_sem_start_date(api_url)
        bmstu_schedule.run(group.get(), sem_start_date, path)
    except SystemExit:
        log.error(f'Schedule for {group.get()} can not be downloaded')
        raise SystemExit


def send_also_available_groups_msg(bot, chat_id, group, available):
    groups = []
    for item in available:
        if item != group.group_type and item != '':
            groups.append(group.name + item)
    ending = 'а' if len(groups) == 1 else 'ы'

    available_groups = ', '.join(groups)
    
    bot.send_message(chat_id, text=replies.AVAILABLE_GROUPS.format(group, ending, available_groups))


def send_choose_group_type_error_msg(bot, chat_id, group, available):
    for item in available:
        item = group.name + item

    available_groups = ', '.join(available)
    bot.send_message(chat_id, text=replies.SPECIFY_GROUP.format(available_groups))


def send_schedule(bot, chat_id, group, path):
    try:
        with open(make_path(path, group, '.ics'), 'rb') as ics:
            with open(make_path(path, group, '.png'), 'rb') as png:
                bot.send_document(chat_id, ics)
                bot.send_photo(chat_id, png)
                bot.send_message(chat_id, text=replies.SCHEDULE_FOUND)
    except FileNotFoundError:
        bot.send_message(chat_id, text=replies.GROUP_NOT_FOUND.format(group))