from typing import List, Optional

from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    category: str = Field(min_length=3)
    year: int = Field(ge=1900)
    rating: float = Field(ge=1, le=10)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "The Shawshank Redemption",
                "category": "Drama",
                "year": 1994,
                "rating": 9.3,
            }
        }


movies = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        "category": "Drama",
        "year": 1994,
        "rating": 9.3,
    },
    {
        "id": 2,
        "title": "The Godfather",
        "category": "Crime",
        "year": 1972,
        "rating": 9.2,
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "category": "Action",
        "year": 2008,
        "rating": 9.0,
    },
    {
        "id": 4,
        "title": "Pulp Fiction",
        "category": "Crime",
        "year": 1994,
        "rating": 8.9,
    },
    {
        "id": 5,
        "title": "Forrest Gump",
        "category": "Drama",
        "year": 1994,
        "rating": 8.8,
    },
    {"id": 6, "title": "Inception", "category": "Action", "year": 2010, "rating": 8.7},
]


@app.get("/", tags=["Home"])
def message():
    return HTMLResponse(content="<h1>Welcome to My Movie API</h1>", status_code=200)


@app.get("/movies", tags=["Movies"], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content={"data": movies})


@app.get("/movies/{id}", tags=["Movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1)) -> Movie:
    movie = next((movie for movie in movies if movie["id"] == id), None)
    if not movie:
        return JSONResponse(content={"error": "Movie not found"}, status_code=404)
    return JSONResponse(content={"data": movie})


@app.get("/movies/", tags=["Movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=3)) -> List[Movie]:
    filtered = next([movie for movie in movies if movie["category"] == category], None)
    return JSONResponse(content={"data": filtered})


@app.post("/movies", tags=["Movies"], response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie.model_dump())
    return JSONResponse(
        content={"message": "Movie created", "data": dict(movie)}, status_code=201
    )


@app.put("/movies/{id}", tags=["Movies"], response_model=dict)
def update_movie(
    id: int,
    movie_update: Movie,
) -> dict:
    movie_dict = next((movie for movie in movies if movie["id"] == id), None)
    if not movie_dict:
        return JSONResponse(content={"error": "Movie not found"}, status_code=404)
    movie_dict["title"] = movie_update.title
    movie_dict["category"] = movie_update.category
    movie_dict["year"] = movie_update.year
    movie_dict["rating"] = movie_update.rating
    return JSONResponse(
        content={"message": "Movie updated", "data": movie_dict},
    )


@app.delete("/movies/{id}", tags=["Movies"], response_model=dict)
def delete_movie(id: int) -> dict:
    movie = next((movie for movie in movies if movie["id"] == id), None)
    if not movie:
        return JSONResponse(content={"error": "Movie not found"}, status_code=404)
    movies.remove(movie)
    return JSONResponse(content={"message": "Movie deleted"})
