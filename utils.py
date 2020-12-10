'''Independent utilities'''
import json
import os
from bs4 import BeautifulSoup
import requests
from logger import LOGGER as Logger

LOGGER = Logger.get_logger('utils')


def get_remote_data(url):
    '''Get data from espn url'''

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    target_script = None
    for script_tag in soup.findAll('script'):
        if '__espnfitt__' in str(script_tag):
            target_script = script_tag
            break
    else:
        err_msg = 'Script not found'
        LOGGER.error(err_msg)
        raise Exception(err_msg)

    data = str(target_script)
    data = '='.join(data.split('=')[2:])
    data = ';'.join(data.split(';')[:-1])

    json_dict = json.loads(data)
    json_dict = json_dict.get("page").get("content")
    return json_dict


def query_local_cache(url, filename, reload=False):
    '''Handle data cache

        Check for cache file
        If hit, load cache
        If miss, run remote func

    '''

    dir_path = '/'.join(filename.split('/')[:-1])
    os.makedirs(dir_path, exist_ok=True)
    if reload is True:
        # force reload cache
        LOGGER.debug(f'Force reload: {url}')
        json_dict = get_remote_data(url)
        with open(filename, 'w') as file:
            json.dump(json_dict, file)
    else:
        try:
            with open(filename, 'r') as file:
                # cache hit
                LOGGER.debug(f'Cache hit: {filename}')
                json_dict = json.load(file)
        except FileNotFoundError:
            # cache miss, reload cache
            LOGGER.debug(f'Cache miss: {url}')
            json_dict = get_remote_data(url)
            with open(filename, 'w') as file:
                json.dump(json_dict, file)
    return json_dict
