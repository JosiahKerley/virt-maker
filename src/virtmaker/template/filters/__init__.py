import os
import string
from pprint import pprint

import psutil
import random
from datetime import date, datetime

import yaml

from virtmaker.config import get_cache_dir
from virtmaker.utils.web import download_file


def filter_year():
    return date.today().strftime("%Y")

def filter_month():
    return date.today().strftime("%m")

def filter_day():
    return date.today().strftime("%d")

def filter_now():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def filter_enumerate(to_enumerate):
    return enumerate(to_enumerate)


## TODO: What is this for?
# def filter_get_param(self, param_name):
#     param = None
#     params_cache_file = os.path.join(self.spec['cachedir'], 'params.cfg')
#     if os.path.exists(params_cache_file):
#         config = configparser.ConfigParser()
#         config.read(params_cache_file)
#         if param_name in config['params'].keys():
#             param = config['params'][param_name]
#     if os.getenv(param_name):
#         param = os.getenv(param_name)
#     if not param:
#         param = input(f"Value for parameter '{param_name}': ")
#         config = configparser.ConfigParser()
#         config['params'][param_name] = param
#         with open(params_cache_file, 'w') as f:
#             config.write(f)
#     return param



def filter_free_memory():
    return int(psutil.virtual_memory().available / 1024 ** 2)

def filter_total_memory():
    return int(psutil.virtual_memory().total / 1024 ** 2)

def filter_at_least(minimum, value):
    if value > minimum:
        return value
    else:
        return minimum

def filter_nproc():
    return os.cpu_count()

def filter_int(number):
    return int(number)

def filter_random_word(max_length=16, min_length=4):
    words_file = '/usr/share/dict/words'
    if not os.path.isfile(words_file):
        raise Exception(f'cannot find file {words_file}')
    with open(words_file) as f:
        words = f.read().splitlines()
    random.shuffle(words)
    allowed_letters = list(string.ascii_lowercase)
    for word in words:
        if min_length <= len(word) <= max_length:
            if all([letter in allowed_letters for letter in list(word)]):
                return word
    raise Exception(f"couldn't find a {max_length} character long word!")

def filter_random_hostname():
    return f'{filter_random_word(max_length=7, min_length=4)}-{filter_random_word(max_length=7, min_length=4)}'

def filter_cache_dir():
    return get_cache_dir()

def filter_file_contents(path, ignore_missing=False):
    if not os.path.isfile(path):
        if ignore_missing:
            return ''
    with open(path) as f:
        return f.read()

def filter_from_yaml(yaml_string):
    return yaml.load(yaml_string, Loader=yaml.Loader)

def filter_download(url, filepath):
    return download_file(url, filepath)
