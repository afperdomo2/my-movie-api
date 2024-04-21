from fastapi import Body, FastAPI
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
    movies_filtered = []
    if category:
        movies_filtered = [movie for movie in movies if movie["category"] == category]
    if year:
        movies_filtered = [movie for movie in movies if movie["year"] == year]
    return {"movies": movies_filtered}


@app.post("/movies", tags=["Movies"])
def create_movie(title: str = Body(), category: str = Body(), year: int = Body()):
    movie_id = len(movies) + 1
    new_movie = {"id": movie_id, "title": title, "category": category, "year": year}
    movies.append(new_movie)
    return {"movie": new_movie}


@app.put("/movies/{movie_id}", tags=["Movies"])
def update_movie(
    movie_id: int, title: str = Body(), category: str = Body(), year: int = Body()
):
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    if not movie:
        return {"error": "Movie not found"}
    movie["title"] = title
    movie["category"] = category
    movie["year"] = year
    return {"movie": movie}


@app.delete("/movies/{movie_id}", tags=["Movies"])
def delete_movie(movie_id: int):
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    if not movie:
        return {"error": "Movie not found"}
    movies.remove(movie)
    return {"movie": movie}
