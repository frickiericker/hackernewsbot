import asyncio
import logging

from hackernewsbot.hackernews import Story, query_new_story_idents

class StoryCollector(object):
    def __init__(self, database):
        self._database = database
        self._query_delay = 0.5

    async def run(self, sleep):
        while True:
            await self.collect_new_stories()
            await asyncio.sleep(sleep)

    async def collect_new_stories(self):
        for story_ident in reversed(query_new_story_idents()):
            await self._insert_story_if_not_exists(story_ident)
            await asyncio.sleep(self._query_delay)

    async def _insert_story_if_not_exists(self, story_ident):
        if self._has_story(story_ident):
            return
        logging.debug('inserting {}'.format(story_ident))
        await self._insert_story(story_ident)

    async def _insert_story(self, story_ident):
        story = await Story.query(story_ident)
        with self._database.cursor() as cursor:
            cursor.execute('INSERT INTO stories (id, time) VALUES (%s, %s);',
                           (story.ident, story.time))
            cursor.execute('INSERT INTO processingStatus (id, processed) VALUES (%s, FALSE);',
                           (story.ident, ))
        self._database.commit()

    def _has_story(self, story_ident):
        with self._database.cursor() as cursor:
            cursor.execute('SELECT * FROM stories WHERE id = %s;',
                           (story_ident, ))
            return cursor.fetchone() is not None
