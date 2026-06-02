import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product


def _order_opts():
    """Return eager-load options for Order queries (customer + items with product)."""
    return (
        joinedload(Order.customer),
        selectinload(Order.items).joinedload(OrderItem.product),
    )


async def _reload(db: AsyncSession, order_id: uuid.UUID) -> Order:
    """Re-fetch an order with all relationships, bypassing the identity-map cache."""
    result = await db.execute(
        select(Order)
        .options(*_order_opts())
        .where(Order.id == order_id)
        .execution_options(populate_existing=True)
    )
    return result.scalar_one()


class OrderRepository:
    """Database queries for the Order and OrderItem entities."""

    def __init__(self, db: AsyncSession):
        """Bind repository to a database session."""
        self.db = db

    async def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        """Return a fully-loaded order by primary key, or None."""
        result = await self.db.execute(
            select(Order).options(*_order_opts()).where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Order]:
        """Return a paginated list of all orders with their relationships loaded."""
        result = await self.db.execute(
            select(Order).options(*_order_opts()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_customer_id(self, customer_id: uuid.UUID) -> list[Order]:
        """Return all orders belonging to a given customer."""
        result = await self.db.execute(
            select(Order)
            .options(*_order_opts())
            .where(Order.customer_id == customer_id)
        )
        return list(result.scalars().all())

    async def get_item(
        self, order_id: uuid.UUID, item_id: uuid.UUID
    ) -> OrderItem | None:
        """Return a specific line item by its ID within a given order, or None."""
        result = await self.db.execute(
            select(OrderItem).where(
                OrderItem.id == item_id, OrderItem.order_id == order_id
            )
        )
        return result.scalar_one_or_none()

    async def create(self, customer_id: uuid.UUID) -> Order:
        """Insert a new draft order with zero total and return the fully-loaded row."""
        order = Order(customer_id=customer_id, total_amount=Decimal("0"))
        self.db.add(order)
        await self.db.commit()
        return await _reload(self.db, order.id)

    async def add_item(self, order: Order, product: Product) -> Order:
        """Add a product line item, update the order total, return reloaded order."""
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
        """Delete a line item, subtract its snapshot price from the total, return reloaded order."""
        order.total_amount = Decimal(str(order.total_amount)) - item.price_snapshot
        await self.db.delete(item)
        await self.db.commit()
        return await _reload(self.db, order.id)

    async def set_status(self, order: Order, new_status: OrderStatus) -> Order:
        """Persist a status change and return the reloaded order."""
        order.status = new_status
        await self.db.commit()
        return await _reload(self.db, order.id)

    async def delete(self, order: Order) -> None:
        """Hard-delete an order and cascade-delete its items."""
        await self.db.delete(order)
        await self.db.commit()
