''' Module for chest related tasks '''
import asyncio
import json
import time

import requests

from .logger import logger
from .loot import get_loot


async def get_acquired_chest_count(connection):
    future = connection.async_get(f'/lol-champ-select/v1/all-grid-champions')
    await asyncio.sleep(0)
    response = future.result()
    if not response.ok:
        return None
    res_json = response.json()
    acquired_chest_count = len(
        [c for c in res_json if c.get('masteryChestGranted', False)])
    logger.info(f'Acquired chest counts: {acquired_chest_count}')
    return acquired_chest_count


def get_available_chest_count(connection):
    try:
        res = connection.get('/lol-collections/v1/inventories/chest-eligibility')
        if res.ok:
            res_json = res.json()
            return res_json.get('earnableChests')
    except (requests.exceptions.RequestException, json.decoder.JSONDecodeError):
        return None
