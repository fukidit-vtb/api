from abc import ABC, abstractmethod

from app.domain.entity.recipe import RecipeShort
from app.domain.entity.recommends import *


class RecommendProvider(ABC):
    @abstractmethod
    async def init_user(self, grades: list[str]) -> UserVector: ...

    @abstractmethod
    async def estimate(self, vector: UserVector, grade: GradeSubmit) -> UserVector: ...

    @abstractmethod
    async def similar_food(self, vector: UserVector, limit: int = 10) -> RecommendAPIList: ...

    @classmethod
    @abstractmethod
    async def update_data(cls, recipes: list[RecipeShort]): ...
