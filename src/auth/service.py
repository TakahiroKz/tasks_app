from sqlalchemy import select
from fastapi import HTTPException
from src.users.models import User
from src.auth.utils import hash_password

from src.auth.utils import verify_password, create_access_token

class AuthService:
    def __init__(self,db):
        self.db = db

    async def login(self, email:str, password:str):
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            return None
        
        valid_password = verify_password(password, user.hashed_password)
        if not valid_password:
            return None
        
        token = create_access_token({
            "sub": str(user.id)
        })

        return token

    async def register(self, email:str, password:str):
        result = await self.db.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = hash_password(password)
        user = User(
            email=email,
            hashed_password=hashed_password
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
        