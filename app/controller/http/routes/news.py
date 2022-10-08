from fastapi import APIRouter, Depends

from app.domain.entity.news import NewsFilter, NewsList, Roles

router = APIRouter(prefix="/news")


@router.get("/", response_model=NewsList)
async def list_(role: Roles, params: NewsFilter = Depends()):
    _ = role
    _ = params
    return []
