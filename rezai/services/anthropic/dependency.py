from typing import AsyncGenerator

from anthropic import Client

from rezai.settings import settings


async def get_anthropic_client() -> AsyncGenerator[Client, None]:
    """
    Dependency function to get the Anthropic client.

    :yield: Anthropic client.
    """
    client = Client(api_key=settings.anthropic_api_key)
    yield client
