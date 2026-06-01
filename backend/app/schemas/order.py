import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator

from app.schemas.customer import CustomerRead


class OrderItemRead(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    price_snapshot: Decimal

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    customer_id: uuid.UUID
    product_ids: list[uuid.UUID]

    @field_validator("product_ids")
    @classmethod
    def at_least_one_product(cls, v: list) -> list:
        if len(v) < 1:
            raise ValueError("Order must contain at least one product")
        return v


class OrderRead(BaseModel):
    id: uuid.UUID
    customer: CustomerRead
    items: list[OrderItemRead]
    total_amount: Decimal
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
