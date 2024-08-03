from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class ContentBlock(BaseModel):
    type: str
    text: Optional[str] = None
    source: Optional[Dict[str, Any]] = None


class Message(BaseModel):
    role: str
    content: Union[str, List[ContentBlock]]


class Usage(BaseModel):
    input_tokens: int
    output_tokens: int


class MessageResponse(BaseModel):
    id: str
    type: str
    role: str
    content: List[ContentBlock]
    model: str
    stop_reason: str
    stop_sequence: Optional[str]
    usage: Usage
