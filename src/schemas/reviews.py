from typing import List
from pydantic import BaseModel


class Review(BaseModel):
    text: str


class BatchReviews(BaseModel):
    reviews: List[str]
