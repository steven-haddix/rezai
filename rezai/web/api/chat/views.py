import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from rezai.agents.restaurant_search_agent import (
    RestaurantAgentContainer,
    get_restaurant_agent_container,
)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    thread_id: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat_with_restaurant_agent(
    request: ChatRequest,
    agent_container: RestaurantAgentContainer = Depends(get_restaurant_agent_container),
) -> StreamingResponse:
    """
    Endpoint for chatting with the restaurant agent.

    This endpoint receives a chat request containing a user's message and processes it using
    the restaurant agent. It returns the assistant's response as a ChatResponse.

    :param request: The ChatRequest containing the user's message.
    :param agent_container: The container for the restaurant agent.
    :return: The ChatResponse containing the assistant's response.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    input_data = {
        "messages": [
            {"role": "user", "content": request.message},
        ],
    }

    result_stream = agent_container.run_graph(
        input_data,
        config=config,  # type: ignore
        stream_mode="values",
    )

    async def stream_results():
        async for result in result_stream:
            if isinstance(result, dict) and "messages" in result:
                for message in result["messages"]:
                    if hasattr(message, "content"):
                        yield json.dumps({"content": message.content}).encode(
                            "utf-8",
                        ) + b"\n"
            elif isinstance(result, str):
                yield json.dumps({"content": result}).encode("utf-8") + b"\n"
            else:
                yield json.dumps({"content": str(result)}).encode("utf-8") + b"\n"

    return StreamingResponse(stream_results(), media_type="application/json")
