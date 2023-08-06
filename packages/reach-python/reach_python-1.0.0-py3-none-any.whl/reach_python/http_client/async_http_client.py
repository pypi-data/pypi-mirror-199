from abc import ABC

import aiohttp

from reach_python.http_client.creator import HTTPClient


class AsyncHTTPClient(HTTPClient, ABC):
    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def post(self, url, data=None):
        async with self._session.post(url, json=data) as resp:
            resp.raise_for_status()
            return await resp.read()

    async def get(self, url):
        async with self._session.get(url) as resp:
            resp.raise_for_status()
            return await resp.read()

    async def put(self, url, data=None):
        async with self._session.put(url, json=data) as resp:
            resp.raise_for_status()
            return await resp.read()

    async def delete(self, url):
        async with self._session.delete(url) as resp:
            resp.raise_for_status()
            return await resp.read()
