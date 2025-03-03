from pydantic import BaseModel


class NewsItem(BaseModel):
    title: str
    description: str
    link: str
    published: str