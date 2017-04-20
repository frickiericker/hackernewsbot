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
DBCLEANER_SLEEP = int(os.environ.get('DBCLEANER_SLEEP', 600))
STORY_WARMUP = int(os.environ.get('STORY_WARMUP', 60 * 60))
STORIES_TO_KEEP = int(os.environ.get('STORIES_TO_KEEP', 1000))

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    collector = StoryCollector(connect_to_database())
    botposter = StoryPoster(connect_to_database(), timedelta(seconds=STORY_WARMUP))
    dbcleaner = DatabaseCleaner(connect_to_database(), STORIES_TO_KEEP)
    tasks = asyncio.gather(
        collector.run(COLLECTOR_SLEEP),
        botposter.run(BOTPOSTER_SLEEP),
        dbcleaner.run(DBCLEANER_SLEEP)
    )
    asyncio.get_event_loop().run_until_complete(tasks)

def connect_to_database():
    uri = urlparse(DATABASE_URL)
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
