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
    logging.getLogger().setLevel(logging.INFO)
    bot = Bot()
    bot.run()

class Bot:
    def __init__(self):
        self._make_collector()
        self._make_cleaner()
        self._make_broker()

    def run():
        tasks = asyncio.gather(
            self._collector.run(COLLECTOR_SLEEP),
            self._cleaner.run(CLEANER_SLEEP),
            self._broker.run(BROKER_SLEEP)
        )
        asyncio.get_event_loop().run_until_complete(tasks)

    def _make_collector(self):
        self._collector = Collector(StoryRepository(DATABASE_URL),
                                    api_wait=HACKERNEWS_API_WAIT)

    def _make_cleaner(self):
        self._cleaner = Cleaner(StoryRepository(DATABASE_URL),
                                stories_to_keep=STORIES_TO_KEEP)

    def _make_broker(self):
        self._broker = Broker(StoryRepository(DATABASE_URL),
                              hold_time=timedelta(seconds=STORY_WARMUP))
        self._set_filter()
        self._set_poster()

    def _set_filter(self):
        self._broker.add_filter(
            lambda story: (len(story.comment) >= STORY_MINIMUM_COMMENTS and
                           story.score >= STORY_MINIMUM_SCORE)
        )

    def _set_poster(self):
        self._broker.add_poster(MastodonPoster(
            instance=MASTODON_INSTANCE,
            client_id=MASTODON_CLIENT_ID,
            client_secret=MASTODON_CLIENT_SECRET,
            email=MASTODON_EMAIL,
            password=MASTODON_PASSWORD
        ))

if __name__ == '__main__':
    main()
