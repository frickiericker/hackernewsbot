import asyncio
from datetime import timedelta
import logging
import os
import psycopg2
from urllib.parse import urlparse

from hackernewsbot.collector import StoryCollector
from hackernewsbot.botposter import StoryPoster
from hackernewsbot.dbcleaner import DatabaseCleaner

DATABASE_URL = os.environ.get('DATABASE_URL', None)
COLLECTOR_SLEEP = int(os.environ.get('COLLECTOR_SLEEP', 300))
BOTPOSTER_SLEEP = int(os.environ.get('BOTPOSTER_SLEEP', 10))
DBCLEANER_SLEEP = int(os.environ.get('DBCLEANER_SLEEP', 500))
STORY_WARMUP = int(os.environ.get('STORY_WARMUP', 60 * 60))
STORY_TTL = int(os.environ.get('STORY_TTL', 12 * 60 * 60))

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    with connect_to_database(DATABASE_URL) as story_database:
        loop = asyncio.get_event_loop()
        tasks = asyncio.gather(
            make_collector(story_database).run(COLLECTOR_SLEEP),
            make_botposter(story_database).run(BOTPOSTER_SLEEP),
            make_dbcleaner(story_database).run(DBCLEANER_SLEEP)
        )
        loop.run_until_complete(tasks)

def make_collector(story_database):
    return StoryCollector(story_database)

def make_botposter(story_database):
    return StoryPoster(story_database, timedelta(seconds=STORY_WARMUP))

def make_dbcleaner(story_database):
    return DatabaseCleaner(story_database, timedelta(seconds=STORY_TTL))

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

if __name__ == '__main__':
    main()
