import asyncio
from datetime import datetime, timedelta, timezone
import json
import logging
import os
from urllib.parse import urlparse

import psycopg2
import requests

DATABASE_URL = os.environ.get('DATABASE_URL', None)
COLLECTOR_SLEEP = os.environ.get('COLLECTOR_SLEEP', 300)
BOTPOSTER_SLEEP = os.environ.get('BOTPOSTER_SLEEP', 10)
BOTPOST_HOLD_TIME = os.environ.get('BOTPOST_HOLD_TIME', 30) # minutes

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.DEBUG)

def main():
    with connect_to_database(DATABASE_URL) as story_database:
        loop = asyncio.get_event_loop()
        tasks = asyncio.gather(
            make_collector(story_database).run(COLLECTOR_SLEEP),
            make_botposter(story_database).run(BOTPOSTER_SLEEP)
        )
        loop.run_until_complete(tasks)

def make_collector(story_database):
    return StoryCollector(story_database)

def make_botposter(story_database):
    return StoryPoster(story_database, timedelta(minutes=BOTPOST_HOLD_TIME))

def connect_to_database(uri):
    uri = urlparse(uri)
    connection = psycopg2.connect(
        database=uri.path[1:],
        user=uri.username,
        password=uri.password,
        host=uri.hostname,
        port=uri.port
    )
    return connection

class StoryCollector(object):
    def __init__(self, database):
        self._database = database

    async def run(self, sleep):
        while True:
            try:
                await self.collect_new_stories()
            except Exception as e:
                LOG.error('error: (story {}) {}'.format(story_ident, e))
            await asyncio.sleep(sleep)

    async def collect_new_stories(self):
        LOG.debug('collecting new stories')
        for story_ident in query_new_story_idents():
            await self._insert_story_if_not_exists(story_ident)

    async def _insert_story_if_not_exists(self, story_ident):
        if self._has_story(story_ident):
            return
        LOG.debug('inserting {}'.format(story_ident))
        self._insert_story(story_ident)

    def _insert_story(self, story_ident):
        story = Story(story_ident)
        with self._database.cursor() as cursor:
            cursor.execute('INSERT INTO stories (id, time) VALUES (%s, %s);',
                           (story.ident, story.time))
        self._database.commit()

    def _has_story(self, story_ident):
        with self._database.cursor() as cursor:
            cursor.execute('SELECT * FROM stories WHERE id = %s;',
                           (story_ident, ))
            return cursor.rowcount != 0

class StoryPoster(object):
    def __init__(self, database, hold_time):
        self._database = database
        self._hold_time = hold_time

    async def run(self, sleep):
        while True:
            await self.post_stories()
            await asyncio.sleep(sleep)

    async def post_stories(self):
        with self._database.cursor() as cursor:
            cursor.execute('SELECT * FROM stories WHERE time < NOW() - INTERVAL %s;',
                           (self._hold_time, ))
            stories = cursor.fetchall()
            LOG.debug('{} stories to post'.format(len(stories)))
            if stories:
                story_ident, submission_time = stories[-1]
                story = Story(story_ident)
                age = datetime.now(timezone.utc) - submission_time
                LOG.debug('Last one: {} | {}'.format(age, story.title))

class Story(object):
    def __init__(self, ident):
        self._ident = ident
        self._init_with_api_response(query_story(ident))

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

# https://github.com/HackerNews/API
API_ROOT = 'https://hacker-news.firebaseio.com/v0'

def query_story(ident):
    response = requests.get('{}/item/{}.json'.format(API_ROOT, ident))
    return json.loads(response.text)

def query_new_story_idents():
    response = requests.get(API_ROOT + '/newstories.json')
    story_idents = json.loads(response.text)
    return story_idents

if __name__ == '__main__':
    main()
