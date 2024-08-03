from typing import AsyncGenerator

from anthropic import Client

from rezai.services.anthropic.service import AnthropicService
from rezai.settings import settings


async def get_anthropic_service() -> AsyncGenerator[AnthropicService, None]:
    """
    Dependency function to get the Anthropic service.

    :yield: Anthropic service.
    """
    client = Client(api_key=settings.anthropic_api_key)
    service = AnthropicService(client)
    yield service
