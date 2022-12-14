from abc import ABC

from app.adapter.recommeds.searcher import digest_instance, inside_instance
from app.adapter.recommeds.trends import trends_items
from app.domain.entity.news import *


class NewsStorage(ABC):
    pass


class NewsService:
    __slots__ = "repo",

    @staticmethod
    async def list_(role: Roles, params: NewsFilter) -> NewsList:
        role_ru: str
        if role == Roles.director:
            role_ru = "Генеральный директор"
        elif role == Roles.accountant:
            role_ru = "Бухгалтер"
        else:
            raise NotImplemented(f"Role {role} doesn't exists")

        pi = [(params.page - 1) * 10, params.page * 10]

        return NewsList(
            digests=DigestsList(
                has_next=False,
                list=[News(id=0, source="undefined", data=i)
                      for i in digest_instance.search(role_ru)[pi[0]:pi[1]]],
                **params.dict(),
            ),
            insides=InsidesList(
                has_next=False,
                list=[Inside(id=0, source="undefined", data=i)
                      for i in inside_instance.search(role_ru)[pi[0]:pi[1]]],
                **params.dict(),
            ),
            trends=TrendsList(
                has_next=False,
                list=[Trend(id=0, source="undefined", data=i)
                      for i in trends_items],
                **params.dict(),
            ),
        )
