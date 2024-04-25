from fastapi import FastAPI

from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routes.auth_routes import auth_routes
from routes.home_routes import home_routes
from routes.movies_routes import movies_routes

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)

app.include_router(home_routes)
app.include_router(auth_routes)
app.include_router(movies_routes)

Base.metadata.create_all(bind=engine)
