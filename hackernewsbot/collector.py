import asyncio
import logging

from bot import LOG
from hackernewsbot.hackernews import Story

class StoryCollector(object):
    def __init__(self, database):
        self._database = database

    async def run(self, sleep):
        while True:
            try:
                await self.collect_new_stories()
            except Exception as e:
                logging.error('error: (story {}) {}'.format(story_ident, e))
            await asyncio.sleep(sleep)

    async def collect_new_stories(self):
        logging.debug('collecting new stories')
        for story_ident in query_new_story_idents():
            await self._insert_story_if_not_exists(story_ident)

    async def _insert_story_if_not_exists(self, story_ident):
        if self._has_story(story_ident):
            return
        logging.debug('inserting {}'.format(story_ident))
        self._insert_story(story_ident)

    def _insert_story(self, story_ident):
        story = Story(story_ident)
        with self._database.cursor() as cursor:
            cursor.execute('INSERT INTO stories (id, time) VALUES (%s, %s);',
                           (story.ident, story.time))
        self._database.commit()

    def _has_story(self, story_ident):
        with self._database.cursor() as cursor:
            cursor.execute('SELECT * FROM stories WHERE id = %s;',
                           (story_ident, ))
            return cursor.rowcount != 0
