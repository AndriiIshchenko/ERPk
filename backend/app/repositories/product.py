import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.product import Product
from app.models.product_history import ProductHistory
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_all(self, include_inactive: bool = False) -> list[Product]:
        stmt = select(Product)
        if not include_inactive:
            stmt = stmt.where(Product.deactivated_at.is_(None))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_ids(self, product_ids: list[uuid.UUID]) -> list[Product]:
        result = await self.db.execute(
            select(Product).where(Product.id.in_(product_ids))
        )
        return list(result.scalars().all())

    async def get_history(self, product_id: uuid.UUID) -> list[ProductHistory]:
        result = await self.db.execute(
            select(ProductHistory)
            .options(joinedload(ProductHistory.changed_by))
            .where(ProductHistory.product_id == product_id)
            .order_by(ProductHistory.changed_at.desc())
        )
        return list(result.scalars().all())

    def _snapshot(self, product: Product, change_type: str, user_id: uuid.UUID) -> ProductHistory:
        return ProductHistory(
            product_id=product.id,
            changed_by_user_id=user_id,
            name=product.name,
            description=product.description,
            price=product.price,
            change_type=change_type,
        )

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update(self, product: Product, data: ProductUpdate, user_id: uuid.UUID) -> Product:
        self.db.add(self._snapshot(product, "update", user_id))
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def deactivate(self, product: Product, user_id: uuid.UUID) -> Product:
        self.db.add(self._snapshot(product, "deactivate", user_id))
        product.deactivated_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def restore(self, product: Product, user_id: uuid.UUID) -> Product:
        self.db.add(self._snapshot(product, "restore", user_id))
        product.deactivated_at = None
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        await self.db.delete(product)
        await self.db.commit()
