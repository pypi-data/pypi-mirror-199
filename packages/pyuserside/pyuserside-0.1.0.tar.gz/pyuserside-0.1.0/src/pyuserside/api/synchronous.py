import json.decoder
import httpx

from ..parser import parse_response


class UsersideCategory:
    def __init__(self, category: str, api: 'UsersideAPI'):
        self._api = api
        self._cat = category

    def __getattr__(self, action: str):
        def method(**kwargs):
            return self._api._request(cat=self._cat,
                                      action=action,
                                      **kwargs)

        return method


class UsersideAPI:
    def __init__(self, url: str, key: str):
        self._url = url
        self._key = key
        self._in_use = 0
        self._session: httpx.Client | None = None

    def _request(self, cat: str, action: str, **kwargs):
        params = {'cat': cat, 'action': action}
        params.update(kwargs)
        response = self._session.get(url='api.php', params=params)
        try:
            content = response.json()
        except json.decoder.JSONDecodeError:
            raise RuntimeError('Non-JSON response')
        if not response.status_code == 200:
            raise RuntimeError(content.get('error', 'No error from Userside'))
        elif not response.text:
            raise RuntimeError('Empty response')
        return parse_response(content)

    def __getattr__(self, item):
        return UsersideCategory(item, self)

    def __enter__(self):
        if (self._in_use == 0) and (not self._session):
            self._session = httpx.Client(base_url=self._url,
                                         params={'key': self._key})
        self._in_use += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._in_use -= 1
        if (self._in_use == 0) and self._session:
            self._session.close()
            self._session = None
