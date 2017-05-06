from datetime import datetime, timezone
import json
import requests

from appenv import HACKERNEWS_TIMEOUT
from .asyncutil import do_async
from .model import Story

API_ROOT = 'https://hacker-news.firebaseio.com/v0'

async def query_story_metadata(story_id):
    api = API_ROOT + '/item/{}.json'.format(story_id)
    response = await do_async(lambda: requests.get(api, timeout=HACKERNEWS_TIMEOUT))
    response.raise_for_status()
    return json.loads(response.text)

async def query_recent_story_ids():
    api = API_ROOT + '/newstories.json'
    response = await do_async(lambda: requests.get(api, timeout=HACKERNEWS_TIMEOUT))
    response.raise_for_status()
    return json.loads(response.text)

async def query_story(story_id):
    return Story(story_id=story_id, **await query_story_metadata(story_id))
