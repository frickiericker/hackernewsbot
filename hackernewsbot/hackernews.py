from datetime import datetime, timezone
import json
import requests

API_ROOT = 'https://hacker-news.firebaseio.com/v0'

def query_story(ident):
    response = requests.get('{}/item/{}.json'.format(API_ROOT, ident))
    return json.loads(response.text)

def query_new_story_idents():
    response = requests.get(API_ROOT + '/newstories.json')
    story_idents = json.loads(response.text)
    return story_idents

class Story(object):
    def __init__(self, ident):
        self._ident = ident
        self._set_properties(**query_story(ident))

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
    def ident(self):
        return self._ident

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
