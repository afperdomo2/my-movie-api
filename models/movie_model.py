from sqlalchemy import Column, Float, Integer, String

from config.database import Base


class MovieModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    category = Column(String)
    year = Column(Integer)
    rating = Column(Float)
