import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.customer import CustomerRead


class OrderItemRead(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    price_snapshot: Decimal

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    customer_id: uuid.UUID


class OrderItemAdd(BaseModel):
    product_id: uuid.UUID


class OrderRead(BaseModel):
    id: uuid.UUID
    customer: CustomerRead
    items: list[OrderItemRead]
    total_amount: Decimal
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
