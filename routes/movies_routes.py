from typing import List

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from schemas.movie import Movie
from services.movie_service import MovieService

movies_routes = APIRouter()


@movies_routes.get(
    "/movies",
    tags=["Movies"],
    response_model=List[Movie],
    dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content={"data": jsonable_encoder(result)})


@movies_routes.get(
    "/movies/{id}",
    tags=["Movies"],
    response_model=Movie,
    dependencies=[Depends(JWTBearer())],
)
def get_movie(id: int = Path(ge=1)) -> Movie:
    db = Session()
    movie = MovieService(db).get_movie(id)
    if not movie:
        return JSONResponse(
            content={"message": "Movie not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(content={"data": jsonable_encoder(movie)})


@movies_routes.get(
    "/movies/",
    tags=["Movies"],
    response_model=List[Movie],
    dependencies=[Depends(JWTBearer())],
)
def get_movies_by_category(category: str = Query(min_length=3)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(content={"data": jsonable_encoder(result)})


@movies_routes.post(
    "/movies",
    tags=["Movies"],
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())],
)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(
        content={"message": "Movie created"},
        status_code=status.HTTP_201_CREATED,
    )


@movies_routes.put(
    "/movies/{id}",
    tags=["Movies"],
    response_model=dict,
    dependencies=[Depends(JWTBearer())],
)
def update_movie(id: int, data: Movie) -> dict:
    db = Session()
    movie = MovieService(db).get_movie(id)
    if not movie:
        return JSONResponse(
            content={"message": "Movie not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    MovieService(db).update_movie(id, data)
    return JSONResponse(content={"message": "Movie updated"})


@movies_routes.delete(
    "/movies/{id}",
    tags=["Movies"],
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(JWTBearer())],
)
def delete_movie(id: int) -> None:
    db = Session()
    movie = MovieService(db).get_movie(id)
    if not movie:
        return JSONResponse(
            content={"message": "Movie not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    MovieService(db).delete_movie(id)
    return status.HTTP_204_NO_CONTENT
