from pydantic import BaseModel


class InputNews(BaseModel):
    source: str
    data: str


__all__ = [
    "InputNews",
]
