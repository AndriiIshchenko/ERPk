import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.customer import CustomerRepository
from app.repositories.order import OrderRepository
from app.repositories.product import ProductRepository
from app.schemas.order import OrderCreate, OrderRead


class OrderService:
    def __init__(self, db: AsyncSession):
        self.repo = OrderRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.product_repo = ProductRepository(db)

    async def list_orders(self) -> list[OrderRead]:
        orders = await self.repo.get_all()
        return [OrderRead.model_validate(o) for o in orders]

    async def get_order(self, order_id: uuid.UUID) -> OrderRead:
        order = await self.repo.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )
        return OrderRead.model_validate(order)

    async def list_by_customer(self, customer_id: uuid.UUID) -> list[OrderRead]:
        orders = await self.repo.get_by_customer_id(customer_id)
        return [OrderRead.model_validate(o) for o in orders]

    async def create_order(self, data: OrderCreate) -> OrderRead:
        customer = await self.customer_repo.get_by_id(data.customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
            )

        products = await self.product_repo.get_by_ids(data.product_ids)
        if len(products) != len(data.product_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more products not found",
            )

        order = await self.repo.create_with_items(data, products)
        return OrderRead.model_validate(order)

    async def delete_order(self, order_id: uuid.UUID) -> None:
        order = await self.repo.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )
        await self.repo.delete(order)
