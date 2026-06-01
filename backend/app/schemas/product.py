import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None


class ProductRead(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    price: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}
