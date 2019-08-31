'''
Configuration file
'''

import json
import os
import requests
from datetime import datetime

CONFIG = {
    'token': os.environ.get('ACCESS_TOKEN'),
    'vault': os.environ.get('VAULT'),
    'dialogue': os.environ.get('DIALOGUE_CFG_PATH'),
    'start_date_api_url': os.environ.get('START_DATE_API_URL'),
    'logfile': os.environ.get('LOG_FILE'),
    'doctors': os.environ.get('DOCTORS'),
}

if not os.path.exists(CONFIG['vault']):
    os.makedirs(CONFIG['vault'])

r = requests.get(url=CONFIG['start_date_api_url'])
start_date_json = r.json()
SEM_START_DATE = datetime.strptime(
    start_date_json['semester_start_date'],
    '%d-%m-%Y'
)

SCHEDULE_ICS = '{}/{}.ics'
SCHEDULE_PNG = '{}/{}.png'
