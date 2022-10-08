from fastapi import APIRouter, Depends

from app.domain.entity.news import NewsFilter, NewsList, Roles
from app.domain.service.news import NewsService

router = APIRouter(prefix="/news")


@router.get("/", response_model=NewsList)
async def list_(
        role: Roles,
        params: NewsFilter = Depends(),
        use_case: NewsService = Depends(),
):
    return await use_case.list_(role, params)
