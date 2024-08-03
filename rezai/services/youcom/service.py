# rezai/services/youcom/service.py
from typing import Any

import httpx

from rezai.settings import settings


class YouComService:
    def __init__(self, api_key: str = settings.youcom_api_key):
        self.api_key = api_key
        self.base_url = "https://api.ydc-index.io"

    async def query_web_llm(self, query: str) -> Any:
        headers = {"X-API-Key": self.api_key}
        params = {"query": query}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/rag",
                params=params,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data

    async def get_ai_snippets_for_query(self, query: str) -> Any:
        headers = {"X-API-Key": self.api_key}
        params = {"query": query}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/search",
                params=params,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data
