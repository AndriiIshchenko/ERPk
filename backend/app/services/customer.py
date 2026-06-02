import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate


class CustomerService:
    """Business logic for customer management."""

    def __init__(self, db: AsyncSession):
        """Bind service to a database session."""
        self.repo = CustomerRepository(db)

    async def _get_or_404(self, customer_id: uuid.UUID) -> Customer:
        """Load a customer by ID or raise 404."""
        customer = await self.repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
            )
        return customer

    async def list_customers(self) -> list[CustomerRead]:
        """Return all customers."""
        customers = await self.repo.get_all()
        return [CustomerRead.model_validate(c) for c in customers]

    async def get_customer(self, customer_id: uuid.UUID) -> CustomerRead:
        """Return a single customer by ID, or raise 404."""
        customer = await self._get_or_404(customer_id)
        return CustomerRead.model_validate(customer)

    async def create_customer(self, data: CustomerCreate) -> CustomerRead:
        """Create a customer; raises 409 if the email is already taken."""
        if await self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A customer with this email already exists",
            )
        customer = await self.repo.create(data)
        return CustomerRead.model_validate(customer)

    async def update_customer(
        self, customer_id: uuid.UUID, data: CustomerUpdate
    ) -> CustomerRead:
        """Update customer fields; raises 409 on duplicate email."""
        customer = await self._get_or_404(customer_id)
        if data.email and data.email != customer.email:
            if await self.repo.get_by_email(data.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A customer with this email already exists",
                )
        customer = await self.repo.update(customer, data)
        return CustomerRead.model_validate(customer)

    async def delete_customer(self, customer_id: uuid.UUID) -> None:
        """Hard-delete a customer by ID; raises 404 if not found."""
        customer = await self._get_or_404(customer_id)
        await self.repo.delete(customer)
