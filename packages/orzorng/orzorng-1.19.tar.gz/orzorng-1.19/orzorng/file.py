# -*- coding: utf-8 -*-

import os
import json


def file_exists(file_name, default=''):
    if not os.path.exists(file_name) or not os.path.getsize(file_name):
        file_write(file_name, default)
        return False

    return True


def file_write(file_name, data='', method='w'):
    with open(file_name, method, encoding='utf-8') as f:
        f.write(data)


def file_read(file_name, default=''):
    data = ''
    if file_exists(file_name, default):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read()

    return data


def file_get_line(file_name):
    return file_read(file_name).splitlines()


def file_set_line(file_name, data):
    file_write(file_name, '\n'.join(data), 'w+')


def file_get_json(file_name, default=None):
    if default is None:
        default = {}

    data = default

    if file_exists(file_name, str(default)):
        data = json.loads(file_read(file_name).strip())

    return data


def file_set_json(file_name, data):
    file_write(file_name, json.dumps(data, indent=2))
