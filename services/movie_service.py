from models.movie_model import MovieModel
from schemas.movie import Movie


class MovieService:
    def __init__(self, db):
        self.db = db

    def get_movies(self):
        return self.db.query(MovieModel).all()

    def get_movie(self, id):
        return self.db.query(MovieModel).filter(MovieModel.id == id).first()

    def get_movie_by_category(self, category):
        return self.db.query(MovieModel).filter(MovieModel.category == category).all()

    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return

    def update_movie(self, id, data: Movie):
        movie = self.get_movie(id)
        movie.title = data.title
        movie.category = data.category
        movie.year = data.year
        movie.rating = data.rating
        self.db.commit()
        return

    def delete_movie(self, id):
        movie = self.get_movie(id)
        self.db.delete(movie)
        self.db.commit()
        return
