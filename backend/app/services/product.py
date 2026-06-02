import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repositories.product import ProductRepository
from app.schemas.product import (
    ProductCreate,
    ProductHistoryRead,
    ProductRead,
    ProductUpdate,
)


class ProductService:
    """Business logic for product catalog management including soft-delete lifecycle."""

    def __init__(self, db: AsyncSession):
        """Bind service to a database session."""
        self.repo = ProductRepository(db)

    async def _get_or_404(self, product_id: uuid.UUID) -> Product:
        """Load a product by ID or raise 404."""
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return product

    async def list_products(self, include_inactive: bool = False) -> list[ProductRead]:
        """Return products; inactive ones excluded unless include_inactive is True."""
        products = await self.repo.get_all(include_inactive=include_inactive)
        return [ProductRead.model_validate(p) for p in products]

    async def get_product(self, product_id: uuid.UUID) -> ProductRead:
        """Return a single product by ID, or raise 404."""
        product = await self._get_or_404(product_id)
        return ProductRead.model_validate(product)

    async def create_product(self, data: ProductCreate) -> ProductRead:
        """Create and return a new active product."""
        product = await self.repo.create(data)
        return ProductRead.model_validate(product)

    async def update_product(
        self, product_id: uuid.UUID, data: ProductUpdate, user_id: uuid.UUID
    ) -> ProductRead:
        """Update product fields and write a history snapshot; 409 if inactive."""
        product = await self._get_or_404(product_id)
        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot edit an inactive product — restore it first",
            )
        product = await self.repo.update(product, data, user_id)
        return ProductRead.model_validate(product)

    async def deactivate_product(
        self, product_id: uuid.UUID, user_id: uuid.UUID
    ) -> ProductRead:
        """Soft-delete a product; raises 409 if already inactive."""
        product = await self._get_or_404(product_id)
        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product is already inactive",
            )
        product = await self.repo.deactivate(product, user_id)
        return ProductRead.model_validate(product)

    async def restore_product(
        self, product_id: uuid.UUID, user_id: uuid.UUID
    ) -> ProductRead:
        """Restore a deactivated product; raises 409 if already active."""
        product = await self._get_or_404(product_id)
        if product.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Product is already active"
            )
        product = await self.repo.restore(product, user_id)
        return ProductRead.model_validate(product)

    async def get_history(self, product_id: uuid.UUID) -> list[ProductHistoryRead]:
        """Return the full audit history for a product, newest first; 404 if missing."""
        await self._get_or_404(product_id)
        history = await self.repo.get_history(product_id)
        return [ProductHistoryRead.model_validate(h) for h in history]
