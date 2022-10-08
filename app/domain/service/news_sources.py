import asyncio
from abc import ABC
from typing import List

from app.domain.entity.news_sources import InputNews
from app.domain.provider.recomends.api import NewsSourceProvider

NEWS_POOL: List[NewsSourceProvider] = [

]


class NewsSourceStorage(ABC):
    pass


class NewsSourcesService:
    __slots__ = ()

    async def update(self):
        await asyncio.gather(
            i.get_news(self.__news_callback)
            for i in NEWS_POOL
        )

    async def __news_callback(self, input_: InputNews):
        raise NotImplemented
