import logging
import requests

class MastodonPoster:
    def __init__(self, **options):
        pass

    async def post(self, story):
        logging.debug('posting {} | {}'.format(story.id, story.title))
