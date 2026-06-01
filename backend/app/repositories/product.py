import uuid

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _with_vendor(self):
        return select(Product).options(joinedload(Product.vendor))

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        result = await self.db.execute(
            self._with_vendor().where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Product]:
        result = await self.db.execute(self._with_vendor().offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_by_ids(self, product_ids: list[uuid.UUID]) -> list[Product]:
        result = await self.db.execute(
            self._with_vendor().where(Product.id.in_(product_ids))
        )
        return list(result.scalars().all())

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product, ["vendor"])
        return product

    async def update(self, product: Product, data: ProductUpdate) -> Product:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await self.db.commit()
        await self.db.refresh(product, ["vendor"])
        return product

    async def delete(self, product: Product) -> None:
        await self.db.delete(product)
        await self.db.commit()
