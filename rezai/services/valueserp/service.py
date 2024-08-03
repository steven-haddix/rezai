# rezai/services/valueserp/service.py
from typing import Any

import httpx

from rezai.settings import settings


class ValueSerpService:
    def __init__(self, api_key: str = settings.valueserp_api_key):
        self.api_key = api_key
        self.base_url = "https://api.valueserp.com/search"

    async def search_places(self, query: str, location: str) -> list[Any]:
        params = {
            "api_key": self.api_key,
            "search_type": "places",
            "q": query,
            "location": location,
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            print(data)
            return data.get("places_results", [])

    async def get_place_details(self, data_cid: str) -> Any:
        params = {
            "api_key": self.api_key,
            "search_type": "place_details",
            "data_cid": data_cid,
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("place_details")
