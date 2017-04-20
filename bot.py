import asyncio
from datetime import timedelta
import logging
import os
import psycopg2
from urllib.parse import urlparse

from hackernewsbot.collector import StoryCollector
from hackernewsbot.botposter import StoryPoster

DATABASE_URL = os.environ.get('DATABASE_URL', None)
COLLECTOR_SLEEP = int(os.environ.get('COLLECTOR_SLEEP', 300))
BOTPOSTER_SLEEP = int(os.environ.get('BOTPOSTER_SLEEP', 10))
BOTPOST_HOLD_TIME = int(os.environ.get('BOTPOST_HOLD_TIME', 60)) # minutes

def main():
    logging.getLogger().setLevel('debug')
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

if __name__ == '__main__':
    main()