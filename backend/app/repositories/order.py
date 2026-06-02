import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product


def _order_opts():
    return (
        joinedload(Order.customer),
        selectinload(Order.items).joinedload(OrderItem.product),
    )


async def _reload(db: AsyncSession, order_id: uuid.UUID) -> Order:
    result = await db.execute(
        select(Order).options(*_order_opts()).where(Order.id == order_id)
    )
    return result.scalar_one()


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        result = await self.db.execute(
            select(Order).options(*_order_opts()).where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Order]:
        result = await self.db.execute(
            select(Order).options(*_order_opts()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_customer_id(self, customer_id: uuid.UUID) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .options(*_order_opts())
            .where(Order.customer_id == customer_id)
        )
        return list(result.scalars().all())

    async def get_item(
        self, order_id: uuid.UUID, item_id: uuid.UUID
    ) -> OrderItem | None:
        result = await self.db.execute(
            select(OrderItem).where(
                OrderItem.id == item_id, OrderItem.order_id == order_id
            )
        )
        return result.scalar_one_or_none()

    async def create(self, customer_id: uuid.UUID) -> Order:
        order = Order(customer_id=customer_id, total_amount=Decimal("0"))
        self.db.add(order)
        await self.db.commit()
        return await _reload(self.db, order.id)

    async def add_item(self, order: Order, product: Product) -> Order:
        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            price_snapshot=product.price,
        )
        self.db.add(item)
        order.total_amount = Decimal(str(order.total_amount)) + product.price
        await self.db.commit()
        return await _reload(self.db, order.id)

    async def remove_item(self, order: Order, item: OrderItem) -> Order:
        order.total_amount = Decimal(str(order.total_amount)) - item.price_snapshot
        await self.db.delete(item)
        await self.db.commit()
        return await _reload(self.db, order.id)

    async def set_status(self, order: Order, new_status: OrderStatus) -> Order:
        order.status = new_status
        await self.db.commit()
        return await _reload(self.db, order.id)

    async def delete(self, order: Order) -> None:
        await self.db.delete(order)
        await self.db.commit()
