import json
import os
import requests


from datetime import datetime



def is_file_exists(path):
    return os.path.isfile(path)

def get_sem_start_date(url):
    r = requests.get(url)
    start_date_json = r.json()

    return datetime.strptime(start_date_json['semester_start_date'], '%d-%m-%Y')
