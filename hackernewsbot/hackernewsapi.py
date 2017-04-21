from datetime import datetime, timezone
import json
import requests

from .asyncutil import do_async

API_ROOT = 'https://hacker-news.firebaseio.com/v0'

async def query_story_metadata(story_id):
    api = API_ROOT + '/item/{}.json'.format(story_id)
    response = await do_async(lambda: requests.get(api))
    response.raise_for_status()
    return json.loads(response.text)

async def query_recent_story_ids():
    api = API_ROOT + '/newstories.json'
    response = await do_async(lambda: requests.get(api))
    response.raise_for_status()
    return json.loads(response.text)

class Story(object):
    @staticmethod
    async def query(story_id):
        story = Story()
        story._id = story_id
        story._set_properties(**await query_story_metadata(story_id))
        return story

    def _set_properties(self, time=None, deleted=False, dead=False, kids=[],
                        score=None, title=None, **others):
        if time:
            self._time = datetime.fromtimestamp(time, timezone.utc)
        else:
            self._time = None
        self._deleted = deleted
        self._dead = dead
        self._comments = kids
        self._score = score
        self._title = title

    @property
    def id(self):
        return self._id

    @property
    def time(self):
        return self._time

    @property
    def deleted(self):
        return self._deleted

    @property
    def dead(self):
        return self._dead

    @property
    def comments(self):
        return self._comments

    @property
    def score(self):
        return self._score

    @property
    def title(self):
        return self._title
