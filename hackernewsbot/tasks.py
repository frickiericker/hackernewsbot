import asyncio
from datetime import datetime, timezone
import logging

from .hackernewsapi import Story, query_recent_story_ids

class Collector:
    def __init__(self, repository, api_wait):
        self._repository = repository
        self._api_wait = api_wait

    async def run(self, sleep):
        while True:
            await self._collect_new_stories()
            await asyncio.sleep(sleep)

    async def _collect_new_stories(self):
        for story_id in reversed(await query_recent_story_ids()):
            await self._insert_story_if_not_exists(story_id)
            await asyncio.sleep(self._api_wait)

    async def _insert_story_if_not_exists(self, story_id):
        if self._repository.has_story(story_id):
            return
        await self._insert_story(story_id)

    async def _insert_story(self, story_id):
        story = await Story.query(story_id)
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
            await self._post_pending_stories()
            await asyncio.sleep(sleep)

    async def _post_pending_stories(self):
        story_ids = self._repository.get_pending_stories(self._hold_time)
        for story_id in story_ids:
            posted = await self._filter_and_post(await Story.query(story_id))
            self._mark_story_processed(story_id)
            if posted:
                await asyncio.sleep(self._posting_wait)

    async def _filter_and_post(self, story):
        for filter_func in self._filters:
            if not filter_func(story):
                logging.info('drop {} - {}'.format(story.id, story.title))
                return False
        for poster in self._posters:
            await poster.post(story)
        return True

    def _mark_story_processed(self, story_id):
        self._repository.mark_story(story_id, processed=True)

