'''
Logger file
'''

import datetime
import telebot
import os

from bmstu_schedule_bot import configs


class Logger:
    def __init__(self, path):
        self.path_to_log_dir = path
        self.message_log_fmt = '{} - [MESSAGE]: {} {} [{}] sent: "{}"'
        self.error_log_fmt = '{} - [ERROR]: {}'
        self.info_log_fmt = '{} - [INFO]: {}'

    def _create_path(self, logfile):
        if len(self.path_to_log_dir) != 0:
            if self.path_to_log_dir[len(self.path_to_log_dir)-1] == '/':
                return self.path_to_log_dir + logfile
            return self.path_to_log_dir + '/' + logfile

    def _update_logfile_path(self):
        current_date = datetime.datetime.now().strftime('%d.%m.%Y') + '.txt'
        self.path_to_logfile = self._create_path(current_date)
        os.makedirs(os.path.dirname(self.path_to_logfile), exist_ok=True)

    def _write(self, msg):
        self._update_logfile_path()
        with open(self.path_to_logfile, 'a') as file:
            file.write(msg + "\n")
            print(msg)

    def log(self, msg):
        log_date = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        log_message = ""
        if (type(msg) is telebot.types.Message):
            log_message = self.message_log_fmt.format(
                log_date,
                msg.chat.first_name,
                msg.chat.last_name,
                msg.chat.username,
                msg.text
            )
        elif isinstance(msg, Exception):
            log_message = self.error_log_fmt.format(log_date, str(msg))
        else:
            log_message = self.info_log_fmt.format(log_date, str(msg))

        self._write(log_message)
