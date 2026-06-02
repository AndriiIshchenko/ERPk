import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserRepository:
    """Database queries for the User entity."""

    def __init__(self, db: AsyncSession):
        """Bind repository to a database session."""
        self.db = db

    async def get_by_id(self, user_id: str | uuid.UUID) -> User | None:
        """Return a user by primary key, or None."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Return a user by unique email, or None."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate) -> User:
        """Hash the password, insert a new user row, and return the persisted instance."""
        user = User(email=data.email, hashed_password=hash_password(data.password))
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
