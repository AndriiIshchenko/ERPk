import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.customer import CustomerRead


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    vendor_id: uuid.UUID


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    vendor_id: uuid.UUID | None = None


class ProductRead(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    price: Decimal
    vendor_id: uuid.UUID
    vendor: CustomerRead
    created_at: datetime

    model_config = {"from_attributes": True}
