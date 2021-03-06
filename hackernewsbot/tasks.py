import asyncio
from datetime import datetime, timezone
import logging

from .asyncutil import do_async
from .hackernewsapi import query_recent_story_ids, query_story

def _log_story(action, story):
    logging.info('{}: {} ({}/{}) - {}'.format(
        action, story.id, story.score, len(story.comments), story.title))

class Collector:
    def __init__(self, repository, api_wait):
        self._repository = repository
        self._api_wait = api_wait

    async def run(self, sleep):
        while True:
            await self._collect_new_stories()
            await asyncio.sleep(sleep)

    async def _collect_new_stories(self):
        for story_id in reversed(query_recent_story_ids()):
            await self._insert_story_if_not_exists(story_id)
            await asyncio.sleep(self._api_wait)

    async def _insert_story_if_not_exists(self, story_id):
        if self._repository.has_story(story_id):
            return
        self._insert_story(story_id)

    def _insert_story(self, story_id):
        story = query_story(story_id)
        self._repository.insert_story(story.id, story.time)

class Cleaner:
    def __init__(self, repository, stories_to_keep):
        self._repository = repository
        self._stories_to_keep = stories_to_keep

    async def run(self, sleep):
        while True:
            self._repository.delete_stale_stories(self._stories_to_keep)
            await asyncio.sleep(sleep)

class Broker:
    def __init__(self, repository, hold_time, posting_wait):
        self._repository = repository
        self._hold_time = hold_time
        self._posting_wait = posting_wait
        self._posters = []
        self._filters = []

    def add_poster(self, poster):
        self._posters.append(poster)

    def add_filter(self, filter_func):
        self._filters.append(filter_func)

    async def run(self, sleep):
        while True:
            await self._process_pending_stories()
            await asyncio.sleep(sleep)

    async def _process_pending_stories(self):
        story_ids = self._repository.get_pending_stories(self._hold_time)
        for story_id in story_ids:
            if await self._process_story(story_id):
                await asyncio.sleep(self._posting_wait)

    async def _process_story(self, story_id):
        story = query_story(story_id)
        posted = self._post_if_viable(story)
        self._mark_story_processed(story_id)
        if posted:
            _log_story('post', story)
        else:
            _log_story('drop', story)

    def _post_if_viable(self, story):
        if self._is_story_viable(story):
            self._post(story)
            return True
        return False

    def _post(self, story):
        for poster in self._posters:
            poster.post(story)

    def _is_story_viable(self, story):
        for filter_func in self._filters:
            if not filter_func(story):
                return False
        return True

    def _mark_story_processed(self, story_id):
        self._repository.mark_story(story_id, processed=True)
