from typing import Any, Dict, Iterable, List, Optional, Union

from anthropic.types import MessageParam
from pydantic import BaseModel


class ContentBlock(BaseModel):
    type: str
    text: Optional[str] = None
    source: Optional[Dict[str, Any]] = None


class Message(BaseModel):
    role: str
    content: Union[str, List[ContentBlock]]


class GenerateRequest(BaseModel):
    model: str
    messages: Iterable[MessageParam]


class GenerateResponse(BaseModel):
    id: str
    type: str
    role: str
    content: List[ContentBlock]
    model: str
    stop_reason: str
    stop_sequence: Optional[str]
    usage: Dict[str, int]
