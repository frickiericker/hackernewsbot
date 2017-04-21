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
            await self.collect_new_stories()
            await asyncio.sleep(sleep)

    async def collect_new_stories(self):
        for story_id in reversed(await query_recent_story_ids()):
            await self._insert_story_if_not_exists(story_id)
            await asyncio.sleep(self._api_wait)

    async def _insert_story_if_not_exists(self, story_id):
        if _self._repository.has_story(story_id):
            return
        await self._insert_story(story_id)

    async def _insert_story(self, story_id):
        logging.debug('inserting {}'.format(story_id))
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
    def __init__(self, repository, hold_time):
        self._repository = repository
        self._hold_time = hold_time
        self._posters = []

    def add_poster(self, poster):
        self._posters.append(poster)

    async def run(self, sleep):
        while True:
            await self.post_stories()
            await asyncio.sleep(sleep)

    async def post_stories(self):
        for story_ident in self._query_feasible_stories():
            logging.debug('posting {}'.format(story_ident))
            self._mark_story_processed(story_ident)

    def _query_feasible_stories(self):
        return self._repository.get_pending_stories(self._hold_time)

    def _mark_story_processed(self, story_ident):
        self._repository.mark_story(story_ident, processed=True)

