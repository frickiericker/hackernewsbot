import asyncio
from datetime import timedelta
import logging
import psycopg2
from urllib.parse import urlparse

from appenv import *
from hackernewsbot.poster import MastodonPoster
from hackernewsbot.tasks import Collector, Cleaner, Broker
from storydb.storydb import StoryRepository

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    collector = Collector(open_story_repository(), HACKERNEWS_API_WAIT)
    cleaner = Cleaner(open_story_repository(), STORIES_TO_KEEP)
    broker = Broker(open_story_repository(), timedelta(seconds=STORY_WARMUP))
    broker.add_poster(make_mastodon_poster())
    tasks = asyncio.gather(
        collector.run(COLLECTOR_SLEEP),
        cleaner.run(CLEANER_SLEEP),
        broker.run(BROKER_SLEEP)
    )
    asyncio.get_event_loop().run_until_complete(tasks)

def open_story_repository():
    return StoryRepository(DATABASE_URL)

def make_mastodon_poster():
    return MastodonPoster(instance=MASTODON_INSTANCE,
                          client_id=MASTODON_CLIENT_ID,
                          client_secret=MASTODON_CLIENT_SECRET,
                          email=MASTODON_EMAIL,
                          password=MASTODON_PASSWORD)

if __name__ == '__main__':
    main()
