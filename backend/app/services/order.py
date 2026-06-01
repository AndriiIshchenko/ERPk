import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderStatus
from app.repositories.customer import CustomerRepository
from app.repositories.order import OrderRepository
from app.repositories.product import ProductRepository
from app.schemas.order import OrderCreate, OrderRead


class OrderService:
    def __init__(self, db: AsyncSession):
        self.repo = OrderRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.product_repo = ProductRepository(db)

    async def _get_or_404(self, order_id: uuid.UUID) -> Order:
        order = await self.repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order

    def _require_draft(self, order: Order) -> None:
        if order.status != OrderStatus.draft:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Order is not in draft — items can only be changed before confirmation",
            )

    async def list_orders(self) -> list[OrderRead]:
        orders = await self.repo.get_all()
        return [OrderRead.model_validate(o) for o in orders]

    async def get_order(self, order_id: uuid.UUID) -> OrderRead:
        order = await self._get_or_404(order_id)
        return OrderRead.model_validate(order)

    async def list_by_customer(self, customer_id: uuid.UUID) -> list[OrderRead]:
        orders = await self.repo.get_by_customer_id(customer_id)
        return [OrderRead.model_validate(o) for o in orders]

    async def create_order(self, data: OrderCreate) -> OrderRead:
        if not await self.customer_repo.get_by_id(data.customer_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        order = await self.repo.create(data.customer_id)
        return OrderRead.model_validate(order)

    async def add_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> OrderRead:
        order = await self._get_or_404(order_id)
        self._require_draft(order)
        if any(item.product_id == product_id for item in order.items):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product is already in this order",
            )
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        order = await self.repo.add_item(order, product)
        return OrderRead.model_validate(order)

    async def remove_item(self, order_id: uuid.UUID, item_id: uuid.UUID) -> OrderRead:
        order = await self._get_or_404(order_id)
        self._require_draft(order)
        item = await self.repo.get_item(order_id, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        order = await self.repo.remove_item(order, item)
        return OrderRead.model_validate(order)

    async def confirm_order(self, order_id: uuid.UUID) -> OrderRead:
        order = await self._get_or_404(order_id)
        self._require_draft(order)
        if not order.items:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Cannot confirm an empty order — add at least one product first",
            )
        order = await self.repo.set_status(order, OrderStatus.pending)
        return OrderRead.model_validate(order)

    async def mark_paid(self, order_id: uuid.UUID) -> OrderRead:
        order = await self._get_or_404(order_id)
        if order.status != OrderStatus.pending:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Only confirmed (pending payment) orders can be marked as paid",
            )
        order = await self.repo.set_status(order, OrderStatus.paid)
        return OrderRead.model_validate(order)

    async def cancel_order(self, order_id: uuid.UUID) -> OrderRead:
        order = await self._get_or_404(order_id)
        if order.status not in (OrderStatus.draft, OrderStatus.pending):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Order is already paid or cancelled",
            )
        order = await self.repo.set_status(order, OrderStatus.cancelled)
        return OrderRead.model_validate(order)

    async def delete_order(self, order_id: uuid.UUID) -> None:
        order = await self._get_or_404(order_id)
        await self.repo.delete(order)
