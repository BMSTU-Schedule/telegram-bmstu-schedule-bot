'''
Configuration file
'''

import json
import os
import requests
from datetime import datetime

CONFIG = {}
with open('config.json', 'r') as f:
    CONFIG = json.loads(f.read())

if not os.path.exists(CONFIG['vault']):
    os.makedirs(CONFIG['vault'])

r = requests.get(url=CONFIG['url_api_start_date'])
start_date_json = r.json()
SEM_START_DATE = datetime.strptime(start_date_json['semester_start_date'], '%d-%m-%Y')

SCHEDULE_ICS = '{}/{}.ics'
SCHEDULE_PNG = '{}/{}.png'
