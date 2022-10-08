from fastapi import APIRouter
from .routes.available import router as available_router
from .routes.news import router as news_router

router = APIRouter(prefix="/v1")

router.include_router(available_router)
router.include_router(news_router)
