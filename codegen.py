'''
Code generation file
'''

import json
import hashlib
from config import CONFIG

answers = {}
with open(CONFIG['dialogue'], 'r') as f:
    answers = json.loads(f.read())

handlers_content = '\'\'\'\nGenerated handlers from dialogue.json\n\'\'\'\n' \
                    'import random\n' \
                    'from bot import BOT\n' \
                    'from logger.logger import logger\n\n' 

decorator_pattern = '@BOT.message_handler(regexp="{}")\n' \
                    'def func{}(message):\n' \
                    '\tlogger(message)\n' \
                    '\tBOT.send_message(message.chat.id, text=random.SystemRandom().choice({}))\n\n'


for key, value in answers.items():
    handlers_content += decorator_pattern.format(key, hashlib.sha224(key.encode()).hexdigest(), value)

with open('handlers2.py', 'w') as f:
    f.write(handlers_content)