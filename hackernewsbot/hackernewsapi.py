import json
import requests

from appenv import HACKERNEWS_API, HACKERNEWS_TIMEOUT
from .asyncutil import do_async
from .model import Story

class HackernewsAPI:
    def __init__(self, root, timeout=None):
        self._root = root
        self._timeout = timeout

    async def _query(self, path):
        response = await do_async(lambda: requests.get(self._root + path,
                                                       timeout=self._timeout))
        response.raise_for_status()
        return json.loads(response.text)

    async def item(self, item_id):
        return await self._query('/item/{}.json'.format(item_id))

    async def newstories(self, item_id):
        return await self._query('/newstories'.format(item_id))

# FIXME: Temporary global for backward-compatibility
_HACKERNEWS_API = HackernewsAPI(HACKERNEWS_API, HACKERNEWS_TIMEOUT)

async def query_recent_story_ids():
    return _HACKERNEWS_API.newstories()

async def query_story_metadata(story_id):
    return _HACKERNEWS_API.item(story_id)

async def query_story(story_id):
    return Story(story_id, **await query_story_metadata(story_id))
