import asyncio

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
            cursor.execute('SELECT max(id) from stories;',
            maximum_id = cursor.fetchone()
            minimum_id = maximum_id - self._stories_to_keep + 1
            cursor.execute('DELETE FROM stories WHERE id < %s;',
                           (minimum_id, ))
        self._database.commit()
