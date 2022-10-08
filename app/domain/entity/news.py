from enum import Enum
from typing import List

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


class NewsList(ListDTO):
    list: List[News]


__all__ = [
    "Roles",
    "News",
    "NewsFilter",
    "NewsList",
]
