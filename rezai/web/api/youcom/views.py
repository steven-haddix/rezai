# rezai/web/api/youcom/views.py
from fastapi import APIRouter, Depends

from rezai.services.youcom.service import YouComService
from rezai.web.api.youcom.schema import (
    GetAISnippetsRequest,
    GetAISnippetsResponse,
    QueryWebLLMRequest,
    QueryWebLLMResponse,
)

router = APIRouter()


@router.post("/query_web_llm", response_model=QueryWebLLMResponse)
async def query_web_llm(
    request: QueryWebLLMRequest,
    youcom_service: YouComService = Depends(),
) -> QueryWebLLMResponse:
    """
    Query the web using the You.com API.

    This endpoint will return the results of querying the web using the provided query.

    :param request: QueryWebLLMRequest
    :param youcom_service: YouComService = Depends()

    :return: QueryWebLLMResponse
    """
    query_results = await youcom_service.query_web_llm(request.query)
    return QueryWebLLMResponse(results=query_results)


@router.post("/get_ai_snippets", response_model=GetAISnippetsResponse)
async def get_ai_snippets(
    request: GetAISnippetsRequest,
    youcom_service: YouComService = Depends(),
) -> GetAISnippetsResponse:
    """
    Get AI-generated snippets using the You.com API.

    This endpoint will return AI-generated snippets based on the provided query.

    :param request: GetAISnippetsRequest
    :param youcom_service: YouComService = Depends()

    :return: GetAISnippetsResponse
    """
    snippets = await youcom_service.get_ai_snippets_for_query(request.query)
    return GetAISnippetsResponse(snippets=snippets)
