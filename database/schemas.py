from typing import Optional
from datetime import date
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    rubrics: str
    text: str
    created_date: Optional[date] = None



class PostService(BaseModel):
    es_index: str = 'posts'
    model = Post




