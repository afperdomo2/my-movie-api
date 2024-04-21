from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    category: str = Field(min_length=3)
    year: int = Field(ge=1900)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "The Shawshank Redemption",
                "category": "Drama",
                "year": 1994,
            }
        }


movies = [
    {"id": 1, "title": "The Shawshank Redemption", "category": "Drama", "year": 1994},
    {"id": 2, "title": "The Godfather", "category": "Crime", "year": 1972},
    {"id": 3, "title": "The Dark Knight", "category": "Action", "year": 2008},
    {"id": 4, "title": "Pulp Fiction", "category": "Crime", "year": 1994},
    {"id": 5, "title": "Forrest Gump", "category": "Drama", "year": 1994},
    {"id": 6, "title": "Inception", "category": "Action", "year": 2010},
]


@app.get("/", tags=["Home"])
def message():
    return HTMLResponse(content="<h1>Welcome to My Movie API</h1>", status_code=200)


@app.get("/movies", tags=["Movies"])
def get_movies():
    return {"movies": movies}


@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int):
    movie = next((movie for movie in movies if movie["id"] == id), None)
    return {"movie": movie}


@app.get("/movies/", tags=["Movies"])
def filter_movies(category: str = None, year: int = None):
    movies_filtered = []
    if category:
        movies_filtered = [movie for movie in movies if movie["category"] == category]
    if year:
        movies_filtered = [movie for movie in movies if movie["year"] == year]
    return {"movies": movies_filtered}


@app.post("/movies", tags=["Movies"])
def create_movie(movie: Movie):
    movies.append(movie)
    return {"movie": movie}


@app.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, movie: Movie):
    movie = next((movie for movie in movies if movie["id"] == id), None)
    if not movie:
        return {"error": "Movie not found"}
    movie["title"] = movie.title
    movie["category"] = movie.category
    movie["year"] = movie.year
    return {"movie": movie}


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int):
    movie = next((movie for movie in movies if movie["id"] == id), None)
    if not movie:
        return {"error": "Movie not found"}
    movies.remove(movie)
    return {"movie": movie}
