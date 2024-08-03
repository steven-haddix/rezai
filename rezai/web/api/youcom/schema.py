# rezai/web/api/youcom/schema.py
from typing import Any

from pydantic import BaseModel


class QueryWebLLMRequest(BaseModel):
    query: str


class QueryWebLLMResponse(BaseModel):
    results: Any


class GetAISnippetsRequest(BaseModel):
    query: str


class GetAISnippetsResponse(BaseModel):
    snippets: Any
