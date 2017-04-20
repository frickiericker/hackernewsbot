from datetime import datetime, timedelta, timezone
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
        self._init_with_api_response(query_story(ident))

    def _init_with_api_response(self, response):
        self._time = datetime.fromtimestamp(response['time'], timezone.utc)
        self._deleted = response.get('deleted', False)
        self._dead = response.get('dead', False)
        self._comments = response.get('kids', [])
        self._score = response.get('score', None)
        self._title = response.get('title', None)

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
