import logging
from datetime import datetime, timezone
import json
import requests

from appenv import MASTODON_TIMEOUT

class MastodonPoster:
    def __init__(self, instance, client_id, client_secret, email, password):
        self._instance = instance
        self._authenticate(client_id, client_secret, email, password)

    def _authenticate(self, client_id, client_secret, email, password):
        response = requests.post(self._instance + '/oauth/token', {
            'grant_type': 'password',
            'scope': 'write',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': email,
            'password': password
        }, timeout=MASTODON_TIMEOUT)
        response_data = json.loads(response.text)
        self._access_token = response_data['access_token']
        self._token_type = response_data['token_type']
        logging.info('auth: {}'.format(response.text))
        response.raise_for_status()

    async def post(self, story):
        logging.info('posting {} | {}-{} | {}'.format(
            story.id, len(story.comments), story.score, story.title
        ))
        now = datetime.now(timezone.utc)
        age = now - story.time
        age_in_minutes = round(age.total_seconds() / 60)
        hackernews_uri = 'https://news.ycombinator.com/item?id={}'.format(story.id)
        text = '{}\n{}\n\n{} comments {} points\n(in {} minutes)'.format(
            story.title, hackernews_uri, len(story.comments), story.score,
            age_in_minutes
        )
        response = requests.post(self._instance + '/api/v1/statuses', {
            'status': text,
            'visibility': 'unlisted'
        }, headers={
            'Authorization': '{} {}'.format(self._token_type, self._access_token)
        }, timeout=MASTODON_TIMEOUT)
        logging.info('response: ' + response.text)
        response.raise_for_status()
