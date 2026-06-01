import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate


class CustomerService:
    def __init__(self, db: AsyncSession):
        self.repo = CustomerRepository(db)

    async def _get_or_404(self, customer_id: uuid.UUID) -> Customer:
        customer = await self.repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer

    async def list_customers(
        self, is_vendor: bool | None = None
    ) -> list[CustomerRead]:
        customers = await self.repo.get_all(is_vendor=is_vendor)
        return [CustomerRead.model_validate(c) for c in customers]

    async def get_customer(self, customer_id: uuid.UUID) -> CustomerRead:
        customer = await self._get_or_404(customer_id)
        return CustomerRead.model_validate(customer)

    async def create_customer(self, data: CustomerCreate) -> CustomerRead:
        customer = await self.repo.create(data)
        return CustomerRead.model_validate(customer)

    async def update_customer(
        self, customer_id: uuid.UUID, data: CustomerUpdate
    ) -> CustomerRead:
        customer = await self._get_or_404(customer_id)

        if data.is_vendor is False and customer.is_vendor is True:
            has_products = await self.repo.has_products(customer_id)
            if has_products:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cannot remove vendor status: customer has associated products",
                )

        customer = await self.repo.update(customer, data)
        return CustomerRead.model_validate(customer)

    async def delete_customer(self, customer_id: uuid.UUID) -> None:
        customer = await self._get_or_404(customer_id)
        await self.repo.delete(customer)
