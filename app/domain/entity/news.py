from enum import Enum
from typing import List

from pydantic import BaseModel

from app.domain.entity.base import FilterDTO, ListDTO
from app.domain.entity.news_sources import InputNews


class Roles(Enum):
    director = "DIRECTOR"
    accountant = "ACCOUNTANT"


class NewsFilter(FilterDTO):
    pass


class News(InputNews):
    id: int


class NewsML(News):
    weights: List[int]


class Digest(News):
    pass


class Inside(News):
    pass


class Trend(News):
    pass


class DigestsList(ListDTO):
    list: List[Digest]


class TrendsList(ListDTO):
    list: List[Trend]


class InsidesList(ListDTO):
    list: List[Inside]


class NewsList(BaseModel):
    digests: DigestsList
    insides: InsidesList
    trends: TrendsList


__all__ = [
    "Roles",
    "News",
    "NewsFilter",
    "NewsList",
    "Digest",
    "DigestsList",
    "Inside",
    "InsidesList",
    "Trend",
    "TrendsList",
]
