import json
import logging
import os
from django.core.cache import cache
from django.conf import settings

ECONT_CACHE_KEY = 'econt_cities_data'
ECONT_MTIME_KEY = 'econt_cities_mtime'
ECONT_CACHE_TIMEOUT = 6 * 60 * 60  # 6 hours (you can change this)
logger = logging.getLogger(__name__)

def get_econt_cities_data(force_reload=False):
    """
    Load Econt cities from cache or file.
    :param force_reload: If True, will ignore cache and reload from file.
    :return: List of city dicts
    """
    file_path = os.path.join(settings.DATA_DIR, 'api', 'econt_cities.json')

    try:
        current_mtime = os.path.getmtime(file_path)
    except FileNotFoundError:
        logger.error(f"Econt cities file not found at {file_path}")
        return {}

    cached_mtime = cache.get(ECONT_MTIME_KEY)
    cached_data = cache.get(ECONT_CACHE_KEY)

    if force_reload or cached_data is None or cached_mtime != current_mtime:
        logger.info(f"Reloading Econt cities data from file (force_reload={force_reload})")

        with open(file_path, 'r', encoding='utf-8') as file:
            cities_data = json.load(file)
            cache.set(ECONT_CACHE_KEY, cities_data)
            cache.set(ECONT_MTIME_KEY, current_mtime)
        return cities_data

    return cached_data


def clear_econt_cities_cache():
    """Clear the cached Econt cities data."""
    cache.delete(ECONT_CACHE_KEY)
    cache.delete(ECONT_MTIME_KEY)