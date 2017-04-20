import asyncio
import logging

class DatabaseCleaner(object):
    def __init__(self, database, stories_to_keep):
        self._database = database
        self._stories_to_keep = stories_to_keep

    async def run(self, sleep):
        while True:
            await self.prune_stale_stories()
            await asyncio.sleep(sleep)

    async def prune_stale_stories(self):
        with self._database.cursor() as cursor:
            cursor.execute('SELECT max(ord) from processingStatus;')
            highest_ord, = cursor.fetchone()
            stale_ord = highest_ord - self._stories_to_keep
            cursor.execute(('DELETE FROM stories USING processingStatus ' +
                            'WHERE stories.id = processingStatus.id ' +
                            'AND processingStatus.ord <= %s;'),
                           (stale_ord, ))
            cursor.execute('DELETE FROM processingStatus WHERE ord <= %s;',
                           (stale_ord, ))
            logging.debug('deleted stories <= {}'.format(stale_ord))
        self._database.commit()
