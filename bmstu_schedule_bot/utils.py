import json
import os
import re
import requests


from datetime import datetime


def is_file_exists(path):
    return os.path.isfile(path)


def get_sem_start_date(url):
    r = requests.get(url)
    start_date_json = r.json()

    return datetime.strptime(start_date_json['semester_start_date'], '%d-%m-%Y')


def get_available_types(vault_path, group):
    regexp = re.compile(r'^{}([а-яА-Я])?.ics'.format(group))
    files = os.listdir(vault_path)
    types = []

    for file in files:
        if regexp.match(file):
            gr_type = file[len(group):len(group)+1]
            types.append(gr_type) if gr_type != '.' else types.append('')
            
    return types


def make_path(path='', filename='', file_format=''): # file_format must include a dot
    if len(path) > 0:
        if path[-1] == '/':
            return f'{path}{filename}{file_format}'
        else:
            return f'{path}/{filename}{file_format}'
    else:
        return f'{filename}{file_format}'