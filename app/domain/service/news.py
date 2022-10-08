from abc import ABC

from app.domain.entity.news import *


class NewsStorage(ABC):
    pass


class NewsService:
    __slots__ = "repo",

    async def list_(self, role: Roles, params: NewsFilter) -> NewsList:
        return NewsList(
            has_next=False,
            list=[],
            **params.dict(),
        )
