import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerRepository:
    """Database queries for the Customer entity."""

    def __init__(self, db: AsyncSession):
        """Bind repository to a database session."""
        self.db = db

    async def get_by_id(self, customer_id: uuid.UUID) -> Customer | None:
        """Return a customer by primary key, or None."""
        result = await self.db.execute(
            select(Customer).where(Customer.id == customer_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Customer | None:
        """Return a customer by unique email, or None."""
        result = await self.db.execute(select(Customer).where(Customer.email == email))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Customer]:
        """Return a paginated list of all customers."""
        result = await self.db.execute(select(Customer).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, data: CustomerCreate) -> Customer:
        """Insert a new customer row and return the persisted instance."""
        customer = Customer(**data.model_dump())
        self.db.add(customer)
        await self.db.commit()
        await self.db.refresh(customer)
        return customer

    async def update(self, customer: Customer, data: CustomerUpdate) -> Customer:
        """Apply partial field updates to an existing customer and commit."""
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(customer, field, value)
        await self.db.commit()
        await self.db.refresh(customer)
        return customer

    async def delete(self, customer: Customer) -> None:
        """Delete a customer row and commit."""
        await self.db.delete(customer)
        await self.db.commit()
