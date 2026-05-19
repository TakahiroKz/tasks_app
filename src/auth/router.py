from fastapi import APIRouter, Depends, HTTPException
from src.auth import service
from src.auth.schemas import LoginRequest, TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.dependencies import get_db

from src.users.schemas import UserResponse
from src.users.schemas import UserCreate
from src.auth.service import AuthService

login_router = APIRouter()

@login_router.post("/login")
async def login_route(
    data:LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    token = await auth_service.login(data.email, data.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@login_router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    return await auth_service.register(user_data.email, user_data.password)