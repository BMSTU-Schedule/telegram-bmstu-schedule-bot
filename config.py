'''
Configuration file
'''

import re
import json
from datetime import datetime

GROUP_CODE_REGEX = r'^[а-яА-Я]{1,4}\d{0,2}\-\d{1,3}[а-яА-Я]?$'
GC_REG_MATCHER = re.compile(GROUP_CODE_REGEX)
DT = datetime.strptime('2018-09-03', '%Y-%m-%d')
SCHEDULE_ICS = '{}/{}.ics'
SCHEDULE_PNG = '{}/{}.png'

CONFIG = {}
with open('config.json', 'r') as f:
    CONFIG = json.loads(f.read())
