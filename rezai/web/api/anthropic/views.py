from anthropic.types import Message
from fastapi import APIRouter, Depends

from rezai.services.anthropic.dependency import get_anthropic_service
from rezai.services.anthropic.service import AnthropicService
from rezai.web.api.anthropic.schema import GenerateRequest

router = APIRouter()


@router.post("/generate", response_model=None)
async def generate_message(
    request: GenerateRequest,
    anthropic_service: AnthropicService = Depends(get_anthropic_service),
) -> Message:
    """
    Generate a message using the Anthropic API.

    This endpoint accepts a GenerateRequest object containing the input messages and
    parameters for generating a response using the Anthropic API.

    :param request: The GenerateRequest object containing the input messages and
        parameters.
    :param anthropic_service: The AnthropicService dependency for generating the
        message.
    :return: The Message object containing the generated message and metadata.
    """
    response = await anthropic_service.generate_message(
        model=request.model,
        messages=request.messages,
        **request.model_dump(exclude_unset=True),
    )
    return response
