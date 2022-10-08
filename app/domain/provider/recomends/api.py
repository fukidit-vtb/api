from abc import ABC, abstractmethod
from typing import Callable, Coroutine, List

from app.domain.entity.news_sources import InputNews


class NewsSourceProvider(ABC):
    @abstractmethod
    async def get_news(
            self,
            news_callback: Callable[[InputNews], Coroutine],
    ): ...
