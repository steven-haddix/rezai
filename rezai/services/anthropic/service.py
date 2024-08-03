from typing import Iterable, List, TypedDict, Union

from anthropic import Client
from anthropic.types import Message, MessageParam


class OptionalParams(TypedDict, total=False):
    top_p: float


class AnthropicService:
    def __init__(self, client: Client):
        self.client = client

    async def generate_message(
        self,
        model: str,
        messages: Iterable[MessageParam],
        max_tokens: int = 1000,
        temperature: float = 0.8,
        top_p: Union[None, float] = None,
        stop_sequences: Union[None, List[str]] = None,
        max_completion_time: Union[None, float] = None,
    ) -> Message:

        optional_params: OptionalParams = {}

        if top_p is not None:
            optional_params["top_p"] = top_p

        return self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
            system="You are a helpful assistant named Claude.",
            temperature=temperature,
            **optional_params,
        )
