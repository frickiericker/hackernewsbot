import asyncio
from datetime import datetime, timezone

from hackernewsbot import LOG
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
        with self._database.cursor() as cursor:
            cursor.execute('SELECT * FROM stories WHERE time < NOW() - INTERVAL %s;',
                           (self._hold_time, ))
            stories = cursor.fetchall()
            LOG.debug('{} stories to post'.format(len(stories)))
            if len(stories) > 20:
                for story_ident, submission_time in stories[-20:]:
                    story = Story(story_ident)
                    if story.deleted or story.dead:
                        continue
                    age = datetime.now(timezone.utc) - submission_time
                    LOG.debug('Last one: {} | {} {} | {}'.format(age, len(story.comments), story.score, story.title))
