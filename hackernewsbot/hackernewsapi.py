import json
import requests

from appenv import HACKERNEWS_API, HACKERNEWS_TIMEOUT
from .model import Story

class HackernewsAPI:
    def __init__(self, root, timeout=None):
        self._root = root
        self._timeout = timeout

    def _query(self, path):
        response = requests.get(self._root + path, timeout=self._timeout)
        response.raise_for_status()
        return json.loads(response.text)

    def item(self, item_id):
        return self._query('/item/{}.json'.format(item_id))

    def newstories(self):
        return self._query('/newstories.json')

# FIXME: Temporary global for backward-compatibility
_HACKERNEWS_API = HackernewsAPI(HACKERNEWS_API, HACKERNEWS_TIMEOUT)

def query_recent_story_ids():
    return _HACKERNEWS_API.newstories()

def query_story_metadata(story_id):
    return _HACKERNEWS_API.item(story_id)

def query_story(story_id):
    return Story(story_id, **query_story_metadata(story_id))
