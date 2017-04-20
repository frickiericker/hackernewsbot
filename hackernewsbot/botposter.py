import asyncio
from datetime import datetime, timezone
import logging

from hackernewsbot.hackernews import Story

class StoryPoster(object):
    def __init__(self, database, hold_time):
        self._database = database
        self._hold_time = hold_time

    async def run(self, sleep):
        while True:
            await self.post_stories()
            await asyncio.sleep(sleep)

    async def post_stories(self):
        for story_ident in self._query_feasible_stories():
            self._mark_story_processed(story_ident)

    def _query_feasible_stories(self):
        with self._database.cursor() as cursor:
            cursor.execute(('SELECT stories.id FROM stories, processingStatus ' +
                            'WHERE stories.time < NOW() - INTERVAL %s ' +
                            'AND NOT processingStatus.processed;'),
                           (self._hold_time, ))
            return [story_ident for story_ident, in cursor]

    def _mark_story_processed(self, story_ident):
        with self._database.cursor() as cursor:
            cursor.execute('UPDATE processingStatus SET processed = TRUE WHERE id = %s;',
                           (story_ident, ))
        self._database.commit()

