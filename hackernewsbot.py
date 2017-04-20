import asyncio
from datetime import datetime, timezone
import json
import os
import urllib.parse as urlparse

import psycopg2
import requests

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

DATABASE_URL = os.environ.get('DATABASE_URL', None)

def main():
    story_database = connect_to_story_database()
    try:
        run(story_database)
    finally:
        story_database.close()

def connect_to_story_database():
    url = urlparse.urlparse(DATABASE_URL)
    connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return connection

def run(story_database):
    cursor = story_database.cursor()
    for story_ident in query_new_story_idents():
        cursor.execute('SELECT * FROM stories WHERE id = %s',
                       (story_ident, ))
        if cursor.rowcount == 0:
            story = Story(story_ident)
            cursor.execute('INSERT INTO stories (id, time) VALUES (%s, %s)',
                           (story.ident, story.time))
    cursor.close()

# https://github.com/HackerNews/API
API_ROOT = 'https://hacker-news.firebaseio.com/v0'

class Story(object):
    def __init__(self, ident):
        response = requests.get('{}/item/{}.json'.format(API_ROOT, ident))
        data = json.loads(response.text)
        self._ident = ident
        self._init_with_api_response(data)

    def _init_with_api_response(self, response):
        self._time = datetime.fromtimestamp(response['time'], timezone.utc)
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
    def comments(self):
        return self._comments

    @property
    def score(self):
        return self._score

    @property
    def title(self):
        return self._title

def query_new_story_idents():
    response = requests.get(API_ROOT + '/newstories.json')
    story_idents = json.loads(response.text)
    return story_idents

if __name__ == '__main__':
    main()
