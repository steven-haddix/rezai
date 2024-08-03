from fastapi.routing import APIRouter

from rezai.web.api import (
    anthropic,
    chat,
    docs,
    dummy,
    echo,
    monitoring,
    redis,
    valueserp,
    youcom,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
api_router.include_router(youcom.router, prefix="/youcom", tags=["youcom"])
api_router.include_router(valueserp.router, prefix="/valueserp", tags=["valueserp"])
api_router.include_router(anthropic.router, prefix="/anthropic", tags=["anthropic"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
