from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from schemas.login import Login
from utils.jwt_manager import create_token

auth_routes = APIRouter()


@auth_routes.post("/login", tags=["Auth"], response_model=dict)
def login(user: Login) -> dict:
    if user.email != "admin@gmail.com" or user.password != "123":
        return JSONResponse(
            content={"error": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    token = create_token({"sub": user.email})
    return JSONResponse(content={"token": token})
