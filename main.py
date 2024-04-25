from fastapi import FastAPI

from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.auth import auth_router
from routers.home import home_router
from routers.movies import movies_router

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)

app.include_router(home_router)
app.include_router(auth_router)
app.include_router(movies_router)

Base.metadata.create_all(bind=engine)
