from typing import Any


class BaseClient:

    def __init__(self, service_name: str, platform_context: dict[str, Any]):
        self.api_url = f'http://localhost:9000'
        self.platform_context = platform_context

    @property
    def _headers(self) -> dict[str, Any]:
        return {
            'Accept-Language': self.platform_context.get('locale'),
            'X-Correlation-Id': self.platform_context.get('correlation_id'),
        }
