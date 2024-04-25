from typing import List

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.movies import Movie as MovieModel
from schemas.movie import Movie

movies_router = APIRouter()


@movies_router.get(
    "/movies",
    tags=["Movies"],
    response_model=List[Movie],
    dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(content={"data": jsonable_encoder(result)})


@movies_router.get(
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


@movies_router.get(
    "/movies/",
    tags=["Movies"],
    response_model=List[Movie],
    dependencies=[Depends(JWTBearer())],
)
def get_movies_by_category(category: str = Query(min_length=3)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content={"data": jsonable_encoder(result)})


@movies_router.post(
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


@movies_router.put(
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


@movies_router.delete(
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
