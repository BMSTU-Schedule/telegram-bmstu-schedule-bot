'''
Code generation file
'''

import json
import hashlib
from bmstu_schedule_bot import configs

answers = {}
with open(configs.CONFIG['dialogue'], 'r') as file:
    answers = json.loads(file.read())

handlers_content = '\'\'\'\nGenerated handlers from dialogue.json\n\'\'\'\n' \
                    'import random\n' \
                    'from bmstu_schedule_bot import BOT\n' \
                    'from bmstu_schedule_bot.logger import logger\n\n' 

decorator_pattern = '@BOT.message_handler(regexp=\'{}\')\n' \
                    'def func{}(message):\n' \
                    '\tlogger.log(message)\n' \
                    '\tBOT.send_message(message.chat.id, text=random.SystemRandom().choice({}))\n\n'


for key, value in answers.items():
    handlers_content += decorator_pattern.format(key, hashlib.sha224(key.encode()).hexdigest(), value)

with open('bmstu_schedule_bot/handlers2.py', 'w') as file:
    file.write(handlers_content)