import os
import re


def get_available_types(vault_path, group):
    regexp = re.compile(r'^{}([а-яА-Я])?.ics'.format(group))
    files = os.listdir(vault_path)
    types = []

    for file in files:
        if regexp.match(file):
            gr_type = file[len(group):len(group)+1]
            types.append(gr_type) if gr_type != '.' else types.append('')
    return types
