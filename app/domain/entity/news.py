import json
from enum import Enum
from typing import List

from pydantic import validator

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

    @validator("weights")
    def transform(self, v, _values, **_kwargs):
        return isinstance(v, str) and json.loads(v) or v


class NewsList(ListDTO):
    list: List[News]


__all__ = [
    "Roles",
    "News",
    "NewsFilter",
    "NewsList",
]
