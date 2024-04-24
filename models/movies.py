from sqlalchemy import Column, Float, Integer, String

from config.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String, nullable=True)
    year = Column(Integer)
    director = Column(String)
    category = Column(String)
    rating = Column(Float)
