from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"

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


@app.get("/movies/{movie_id}", tags=["Movies"])
def get_movie(movie_id: int):
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    return {"movie": movie}


@app.get("/movies/", tags=["Movies"])
def filter_movies(category: str = None, year: int = None):
    moviesFiltered = []
    if category:
        moviesFiltered = [movie for movie in movies if movie["category"] == category]
    if year:
        moviesFiltered = [movie for movie in movies if movie["year"] == year]
    return {"movies": moviesFiltered}
