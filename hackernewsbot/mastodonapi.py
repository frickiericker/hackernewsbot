import logging
import json
import requests

class MastodonAPI:
    def __init__(self, instance, timeout=None):
        self._instance = instance
        self._timeout = timeout

    def _post(self, path, arg, **kwargs):
        response = requests.post(self._instance + path, arg,
                                 timeout=self._timeout, **kwargs)
        response.raise_for_status()
        return json.loads(response.text)

    def _post_with_auth(self, path, arg):
        return self._post(path, arg, headers={
            'Authorization': '{} {}'.format(self._token_type,
                                            self._access_token)
        })

    def authenticate(self, client_id, client_secret, email, password):
        response = self._post('/oauth/token', {
            'grant_type': 'password',
            'scope': 'write',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': email,
            'password': password
        })
        self._access_token = response['access_token']
        self._token_type = response['token_type']
        return self

    def post_status(self, args):
        self._post_with_auth('/api/v1/statuses', args)
