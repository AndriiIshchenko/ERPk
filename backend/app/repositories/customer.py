import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, customer_id: uuid.UUID) -> Customer | None:
        result = await self.db.execute(
            select(Customer).where(Customer.id == customer_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_vendor: bool | None = None,
    ) -> list[Customer]:
        stmt = select(Customer)
        if is_vendor is not None:
            stmt = stmt.where(Customer.is_vendor == is_vendor)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, data: CustomerCreate) -> Customer:
        customer = Customer(**data.model_dump())
        self.db.add(customer)
        await self.db.commit()
        await self.db.refresh(customer)
        return customer

    async def update(self, customer: Customer, data: CustomerUpdate) -> Customer:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(customer, field, value)
        await self.db.commit()
        await self.db.refresh(customer)
        return customer

    async def delete(self, customer: Customer) -> None:
        await self.db.delete(customer)
        await self.db.commit()

    async def has_products(self, customer_id: uuid.UUID) -> bool:
        from app.models.product import Product

        result = await self.db.execute(
            select(Product).where(Product.vendor_id == customer_id).limit(1)
        )
        return result.scalar_one_or_none() is not None
