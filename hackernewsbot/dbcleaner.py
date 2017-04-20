import asyncio

class DatabaseCleaner(object):
    def __init__(self, database, time_to_live):
        self._database = database
        self._time_to_live = time_to_live

    async def run(self, sleep):
        while True:
            await self.prune_stale_stories()
            await asyncio.sleep(sleep)

    async def prune_stale_stories(self):
        with self._database.cursor() as cursor:
            cursor.execute('DELETE * FROM stories WHERE time < NOW() - INTERVAL %s;',
                           (self._time_to_live, ))
        self._database.commit()
