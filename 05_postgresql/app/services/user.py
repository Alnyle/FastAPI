from fastapi import HTTPException, status
from sqlalchemy import select

from .base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
import bcrypt

from utils import generate_access_token


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed.encode("utf-8"),
    )


class UserService(BaseService):


    def __int__(self, model: User, session: AsyncSession):

        self.model = model
        self.session = session


    async def _add_user(self, data: dict):

        user = self.model(
            **data,
            password_hash=hash_password(data['password'])
        )

        return await self._add(user)

    async def _get_by_email(self, email) -> User | None:

        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email, password) -> str:


        # validate the credientials
        user = await self._get_by_email(email)

        
        # if the seller is not found or the password is incorrect, raise an HTTPException
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )


        token = generate_access_token(data={
            "user": {
                "name": user.name,
                "id": str(user.id),
            }
        })

        return token