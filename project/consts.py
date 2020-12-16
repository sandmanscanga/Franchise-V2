'''Module to store project constants'''
import os


LOG_LEVEL = 10  # logging.DEBUG
PROJECT_PATH = os.path.sep.join(__file__.split(os.path.sep)[:-1])
CACHE_BASE = f"{PROJECT_PATH}/cache"
BASE_URL = "https://www.espn.com"
