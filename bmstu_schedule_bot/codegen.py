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
                    'from bmstu_schedule_bot import bot\n' \
                    'from bmstu_schedule_bot import logger\n\n\n'

decorator_pattern = '@bot.message_handler(regexp=\'{}\')\n' \
                    'def func{}(message):\n' \
                    '    logger.log(message)\n' \
                    '    bot.send_message(\n' \
                    '        message.chat.id,\n' \
                    '        text=random.SystemRandom().choice({}))\n\n\n'


for key, value in answers.items():
    handlers_content += decorator_pattern.format(
        key, hashlib.sha224(key.encode()).hexdigest(), value)

with open('bmstu_schedule_bot/handlers2.py', 'w') as file:
    file.write(handlers_content[:len(handlers_content)-2])
