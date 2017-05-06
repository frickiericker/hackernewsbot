import logging
import json
import requests

from appenv import MASTODON_TIMEOUT

MESSAGE_TEMPLATE = '{title}\n{uri}\n{score} | {comments}'

def plural(number, thing):
    if number == 1:
        return '{} {}'.format(number, thing)
    else:
        return '{} {}s'.format(number, thing)


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
        response.raise_for_status()

    async def post(self, story):
        logging.info('post {} ({}/{}) - {}'.format(
            story.id, story.score, len(story.comments), story.title
        ))
        text = MESSAGE_TEMPLATE.format(
            title=story.title,
            uri=story.uri,
            score=plural(story.score, 'point'),
            comments=plural(len(story.comments), 'comment')
        )
        response = requests.post(self._instance + '/api/v1/statuses', {
            'status': text,
            'visibility': 'unlisted'
        }, headers={
            'Authorization': '{} {}'.format(self._token_type,
                                            self._access_token)
        }, timeout=MASTODON_TIMEOUT)
        response.raise_for_status()
