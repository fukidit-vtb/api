from enum import Enum
from typing import List

from pydantic import BaseModel

from app.domain.entity.base import FilterDTO, ListDTO


class Roles(Enum):
    director = "DIRECTOR"
    accountant = "ACCOUNTANT"


class NewsFilter(FilterDTO):
    pass


class News(BaseModel):
    pass


class NewsList(ListDTO):
    list: List[News]
