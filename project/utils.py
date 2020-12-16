'''Independent utilities'''
import json
import os
from bs4 import BeautifulSoup
import requests
from project.logger import LOGGER as Logger
import project.consts

LOGGER = Logger.get_logger('utils')


def build_cache_path(path, *paths):
    """Build full cache path"""

    path_tup = (project.consts.CACHE_BASE, path) + paths
    cache_path = os.path.sep.join(path_tup)
    return cache_path


def make_cache_dir(cache_path):
    """Creates cache directory"""

    sep = os.path.sep
    dir_paths = cache_path.split(sep)[:-1]
    dir_path = sep.join(dir_paths)
    os.makedirs(dir_path, exist_ok=True)


def get_remote_data(url):
    '''Get data from espn url'''

    LOGGER.debug(f"Getting remote url: {url}")
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


def query_local_cache(url, cache_path, reload=False):
    '''Handle data cache

        Check for cache file
        If hit, load cache
        If miss, run remote func

    '''

    make_cache_dir(cache_path)
    if reload is True:
        # force reload cache
        LOGGER.debug(f'Force reload: {url}')
        json_dict = get_remote_data(url)
        with open(cache_path, 'w') as file:
            json.dump(json_dict, file)
    else:
        try:
            with open(cache_path, 'r') as file:
                # cache hit
                LOGGER.debug(f'Cache hit: {cache_path}')
                json_dict = json.load(file)
        except FileNotFoundError:
            # cache miss, reload cache
            LOGGER.debug(f'Cache miss: {cache_path}')
            json_dict = get_remote_data(url)
            with open(cache_path, 'w') as file:
                json.dump(json_dict, file)
    return json_dict
