from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"

movies = [
    {"title": "The Shawshank Redemption", "director": "Frank Darabont", "year": 1994},
    {"title": "The Godfather", "director": "Francis Ford Coppola", "year": 1972},
    {"title": "The Dark Knight", "director": "Christopher Nolan", "year": 2008},
]


@app.get("/", tags=["Home"])
def message():
    return HTMLResponse(content="<h1>Welcome to My Movie API</h1>", status_code=200)


@app.get("/movies", tags=["Movies"])
def getMovies():
    return {"movies": movies}
