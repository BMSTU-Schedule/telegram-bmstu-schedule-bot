'''
Configuration file
'''

import re
import json
import requests
from datetime import datetime

CONFIG = {}
with open('config.json', 'r') as f:
    CONFIG = json.loads(f.read())

GROUP_CODE_REGEX = r'^[а-яА-Я]{1,4}\d{0,2}\-\d{1,3}[а-яА-Я]?$'
GC_REG_MATCHER = re.compile(GROUP_CODE_REGEX)
r = requests.get(url=CONFIG['url_api_start_date'])
start_date_json = r.json()

DT = datetime.strptime(start_date_json['semester_start_date'], '%d-%m-%Y')
SCHEDULE_ICS = '{}/{}.ics'
SCHEDULE_PNG = '{}/{}.png'
