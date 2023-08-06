from typing import Any

import httpx
from . import BaseClient


class HttpxClient(BaseClient):

    def get(self, path: str, params: dict[str, Any] = None, raises: bool = False, **kwargs):
        if params is None:
            params = {}

        return self._request(
            method='get',
            path=path,
            params=params,
            raises=raises,
            **kwargs,
        )

    def post(self, path: str, data: dict[str, Any], raises: bool = False, **kwargs):
        return self._request(
            method='get',
            path=path,
            data=data,
            raises=raises,
            **kwargs,
        )

    def _request(self, method: str, path: str, raises: bool = False, **kwargs) -> httpx.Response:
        with httpx.Client(headers=self._headers) as client:
            kwargs['headers'] = {**self._headers, **kwargs.get('headers', {})}

            try:
                resp = getattr(client, method)(f'{self.api_url}/{path}', **kwargs)

                return (resp, None) if not raises else resp
            except BaseException as e:
                print(e)


class AsyncHttpxClient(BaseClient):

    async def get(self, path: str):
        return await self._request(method='get', path=path)

    async def post(self, path: str):
        return await self._request(method='post', path=path)

    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient(headers=self._headers) as client:
            return getattr(client, method)(path)
