from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from jwt_manager import create_token
from schemas.user_login import UserLogin

auth_router = APIRouter()


@auth_router.post("/login", tags=["Auth"], response_model=dict)
def login(user: UserLogin) -> dict:
    if user.email != "admin@gmail.com" or user.password != "123":
        return JSONResponse(
            content={"error": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    token = create_token({"sub": user.email})
    return JSONResponse(content={"token": token})
