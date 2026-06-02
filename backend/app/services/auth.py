from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, Token


class AuthService:
    """Business logic for user registration and authentication."""

    def __init__(self, db: AsyncSession):
        """Bind service to a database session."""
        self.repo = UserRepository(db)

    async def register(self, data: UserCreate) -> Token:
        """Create a new user and return a JWT; raises 409 if the email is taken."""
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        user = await self.repo.create(data)
        token = create_access_token({"sub": str(user.id)})
        return Token(access_token=token)

    async def login(self, email: str, password: str) -> Token:
        """Verify credentials and return a JWT; raises 401 on bad email or password."""
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        token = create_access_token({"sub": str(user.id)})
        return Token(access_token=token)
