'''
Logger file
'''

import datetime
import telebot
import os

from bmstu_schedule_bot import configs

class Logger:
	def __init__(self, path):
		self.path_to_file = path
		self.message_log_fmt = '{} - [MESSAGE]: {} {} [{}] sent: "{}"'
		self.error_log_fmt = '{} - [ERROR]: {}'
		self.info_log_fmt = '{} - [INFO]: {}'
	
	def _write(self, msg):
		with open(self.path_to_file, 'a') as file:
			file.write(msg + "\n")
			print(msg)

	def log(self, msg):
		log_date = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
		log_message = ""
		if (type(msg) is telebot.types.Message):
			log_message = self.message_log_fmt.format(log_date, msg.chat.first_name, msg.chat.last_name, msg.chat.username, msg.text)
		elif isinstance(msg, Exception):
			log_message = self.error_log_fmt.format(log_date, str(msg))
		else:
			log_message = self.info_log_fmt.format(log_date, str(msg))

		self._write(log_message)


# Creating folder "/%path%/log" if not exist and creating logfile, which is named "%current_date%.txt"
current_date = datetime.datetime.now().strftime('%d.%m.%Y')
log_file_path = configs.CONFIG['logfile'].format(current_date)
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logger = Logger(log_file_path)