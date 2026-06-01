import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate


def _order_options():
    return (
        joinedload(Order.customer),
        selectinload(Order.items),
    )


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        result = await self.db.execute(
            select(Order)
            .options(*_order_options())
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Order]:
        result = await self.db.execute(
            select(Order).options(*_order_options()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_customer_id(self, customer_id: uuid.UUID) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .options(*_order_options())
            .where(Order.customer_id == customer_id)
        )
        return list(result.scalars().all())

    async def create_with_items(
        self, data: OrderCreate, products: list[Product]
    ) -> Order:
        total = sum(p.price for p in products)
        order = Order(
            customer_id=data.customer_id,
            total_amount=Decimal(str(total)),
        )
        self.db.add(order)
        await self.db.flush()

        for product in products:
            item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                price_snapshot=product.price,
            )
            self.db.add(item)

        await self.db.commit()
        await self.db.refresh(order)

        result = await self.db.execute(
            select(Order)
            .options(*_order_options())
            .where(Order.id == order.id)
        )
        return result.scalar_one()

    async def delete(self, order: Order) -> None:
        await self.db.delete(order)
        await self.db.commit()
