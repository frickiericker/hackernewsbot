import logging
import json
import requests

class MastodonPoster:
    def __init__(self, instance, client_id, client_secret, email, password):
        self._instance = instance
        self._authenticate(client_id, client_secret, email, password)

    def _authenticate(self, client_id, client_secret, email, password):
        response = requests.post(self._instance + '/oauth/token', {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': email,
            'password': password
        })
        print(response.text)

#curl -X POST \
#     -d "client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&grant_type=password&username=${EMAIL}&password=${PASSWORD}" \
#     -Ss "${INSTANCE}/oauth/token"
    async def post(self, story):
        logging.info('posting {} | {}-{} | {}'.format(
            story.id, len(story.comments), story.score, story.title
        ))
