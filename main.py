from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"

movies = [
    {"id": 1, "title": "The Shawshank Redemption", "year": 1994},
    {"id": 2, "title": "The Godfather", "year": 1972},
    {"id": 3, "title": "The Dark Knight", "year": 2008},
    {"id": 4, "title": "The Lord of the Rings: The Return of the King", "year": 2003},
    {"id": 5, "title": "Pulp Fiction", "year": 1994},
    {"id": 6, "title": "Forrest Gump", "year": 1994},
]


@app.get("/", tags=["Home"])
def message():
    return HTMLResponse(content="<h1>Welcome to My Movie API</h1>", status_code=200)


@app.get("/movies", tags=["Movies"])
def getMovies():
    return {"movies": movies}


@app.get("/movies/{movie_id}", tags=["Movies"])
def getMovie(movie_id: int):
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    return {"movie": movie}
