from fastapi import APIRouter
from fastapi.responses import HTMLResponse

home_routes = APIRouter()


@home_routes.get("/", tags=["Home"])
def message():
    return HTMLResponse(content="<h1>Welcome to My Movie API</h1>", status_code=200)
