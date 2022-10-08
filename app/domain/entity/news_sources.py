from pydantic import BaseModel


class InputNews(BaseModel):
    source: str
    title: str
    body: str


__all__ = [
    "InputNews",
]
