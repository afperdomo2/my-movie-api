from typing import List, Optional

from fastapi import Depends, FastAPI, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from config.database import Base, Session, engine
from jwt_manager import create_token
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from models.movies import Movie as MovieModel

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)


Base.metadata.create_all(bind=engine)


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "password": "123",
            }
        }


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


@app.post("/login", tags=["Auth"], response_model=dict)
def login(user: UserLogin) -> dict:
    if user.email != "admin@gmail.com" or user.password != "123":
        return JSONResponse(
            content={"error": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    token = create_token({"sub": user.email})
    return JSONResponse(content={"token": token})


@app.get("/", tags=["Home"])
def message():
    return HTMLResponse(content="<h1>Welcome to My Movie API</h1>", status_code=200)


@app.get(
    "/movies",
    tags=["Movies"],
    response_model=List[Movie],
    dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(content={"data": jsonable_encoder(result)})


@app.get(
    "/movies/{id}",
    tags=["Movies"],
    response_model=Movie,
    dependencies=[Depends(JWTBearer())],
)
def get_movie(id: int = Path(ge=1)) -> Movie:
    db = Session()
    movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not movie:
        return JSONResponse(
            content={"message": "Movie not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(content={"data": jsonable_encoder(movie)})


@app.get(
    "/movies/",
    tags=["Movies"],
    response_model=List[Movie],
    dependencies=[Depends(JWTBearer())],
)
def get_movies_by_category(category: str = Query(min_length=3)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content={"data": jsonable_encoder(result)})


@app.post(
    "/movies",
    tags=["Movies"],
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())],
)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(
        content={"message": "Movie created"},
        status_code=status.HTTP_201_CREATED,
    )


@app.put(
    "/movies/{id}",
    tags=["Movies"],
    response_model=dict,
    dependencies=[Depends(JWTBearer())],
)
def update_movie(
    id: int,
    movie_update: Movie,
) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(
            content={"message": "Movie not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    result.title = movie_update.title
    result.category = movie_update.category
    result.year = movie_update.year
    result.rating = movie_update.rating
    db.commit()
    return JSONResponse(content={"message": "Movie updated"})


@app.delete(
    "/movies/{id}",
    tags=["Movies"],
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(JWTBearer())],
)
def delete_movie(id: int) -> None:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(
            content={"message": "Movie not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    db.delete(result)
    db.commit()
    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)
