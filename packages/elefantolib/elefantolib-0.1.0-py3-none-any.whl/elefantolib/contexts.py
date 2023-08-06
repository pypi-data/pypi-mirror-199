from abc import ABC
from typing import Any

from http_client import httpx_client

import providers


class BaseContext(ABC):
    HTTP_CLIENT = None
    CONTEXT_ATTRIBUTES = (
        'auth_token',
        'correlation_id',
        'locale',
    )

    def __init__(self, provider: providers.Provider):
        for attribute in self.CONTEXT_ATTRIBUTES:
            setattr(self, attribute, getattr(provider, attribute, None))

        self.services = ContextServices(self.HTTP_CLIENT, self.context)

    @property
    def context(self):
        return {a: getattr(self, a) for a in self.CONTEXT_ATTRIBUTES}


class PlatformContext(BaseContext):
    HTTP_CLIENT = httpx_client.HttpxClient


class AsyncPlatformContext(BaseContext):
    HTTP_CLIENT = httpx_client.AsyncHttpxClient


class ContextServices:

    def __init__(self, client, context: dict[str, Any]):
        self._client = client
        self._context = context

    def __getattr__(self, item):
        service = self._client(service_name=item, platform_context=self._context)
        setattr(self, item, service)

        return service

    def __getitem__(self, item):
        return getattr(self, item)
