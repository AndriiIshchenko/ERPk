import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    is_vendor: bool = False


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    is_vendor: bool | None = None


class CustomerRead(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    phone: str | None
    is_vendor: bool
    created_at: datetime

    model_config = {"from_attributes": True}
