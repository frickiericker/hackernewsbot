import asyncio
from datetime import datetime, timedelta, timezone
import logging

from appenv import *
from hackernewsbot.mastodonapi import MastodonAPI
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

    def run(self):
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
                              hold_time=timedelta(seconds=STORY_WARMUP),
                              posting_wait=POSTING_WAIT)
        self._set_filter()
        self._set_poster()

    def _set_filter(self):
        self._add_moderation_filter()
        self._add_cooldown_filter()
        self._add_score_filter()

    def _add_moderation_filter(self):
        self._broker.add_filter(
            lambda story:
                not (story.dead or story.deleted)
        )

    def _add_cooldown_filter(self):
        self._broker.add_filter(
            lambda story:
                (datetime.now(timezone.utc) - story.time)
                    .total_seconds() < STORY_COOLDOWN
        )

    def _add_score_filter(self):
        self._broker.add_filter(
            lambda story:
                len(story.comments) >= STORY_MINIMUM_COMMENTS and
                story.score >= STORY_MINIMUM_SCORE
        )

    def _set_poster(self):
        self._add_main_poster()
        self._add_sub_poster()

    def _add_main_poster(self):
        mastodon = MastodonAPI(MASTODON_INSTANCE, MASTODON_TIMEOUT)
        mastodon.authenticate(
            client_id=MASTODON_CLIENT_ID,
            client_secret=MASTODON_CLIENT_SECRET,
            email=MASTODON_EMAIL,
            password=MASTODON_PASSWORD)
        self._broker.add_poster(MastodonPoster(mastodon))

    def _add_sub_poster(self):
        if not MASTODON_INSTANCE_2:
            return
        mastodon = MastodonAPI(MASTODON_INSTANCE_2, MASTODON_TIMEOUT)
        mastodon.authenticate(
            client_id=MASTODON_CLIENT_ID_2,
            client_secret=MASTODON_CLIENT_SECRET_2,
            email=MASTODON_EMAIL_2,
            password=MASTODON_PASSWORD_2)
        self._broker.add_poster(MastodonPoster(mastodon))

if __name__ == '__main__':
    main()
