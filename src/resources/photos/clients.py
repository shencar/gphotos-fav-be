import functools
from contextlib import asynccontextmanager
from functools import cached_property

import google
import google.oauth2._credentials_async
import google.oauth2.credentials
import googleapiclient
import googleapiclient.discovery
from google.auth.transport._aiohttp_requests import AuthorizedSession as AuthorizedSessionAsync


class GooglePhotosClient:
    API_SERVICE_NAME = "photoslibrary"
    API_VERSION = "v1"

    def __init__(self, credentials: dict):
        self.credentials = credentials
        self._session = None

    @cached_property
    def _client(self):
        credentials = google.oauth2.credentials.Credentials(**self.credentials)
        return googleapiclient.discovery.build(
            self.API_SERVICE_NAME,
            self.API_VERSION,
            static_discovery=False,
            credentials=credentials
        )

    @staticmethod
    def authed_session(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            credentials = google.oauth2._credentials_async.Credentials(**self.credentials)
            async with AuthorizedSessionAsync(credentials) as session:
                self._session = session
                try:
                    return await func(self, *args, **kwargs)
                finally:
                    self._session = None
        return wrapper

    @authed_session
    async def foo(self):
        pass

    def __hash__(self):
        return hash(self.credentials)
