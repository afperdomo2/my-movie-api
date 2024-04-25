from typing import Optional

from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    category: str = Field(min_length=3)
    year: int = Field(ge=1900)
    rating: float = Field(ge=1, le=10)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Shawshank Redemption",
                "category": "Drama",
                "year": 1994,
                "rating": 9.3,
            }
        }
