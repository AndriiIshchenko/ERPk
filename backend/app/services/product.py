import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repositories.customer import CustomerRepository
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate


class ProductService:
    def __init__(self, db: AsyncSession):
        self.repo = ProductRepository(db)
        self.customer_repo = CustomerRepository(db)

    async def _get_or_404(self, product_id: uuid.UUID) -> Product:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    async def list_products(self) -> list[ProductRead]:
        products = await self.repo.get_all()
        return [ProductRead.model_validate(p) for p in products]

    async def get_product(self, product_id: uuid.UUID) -> ProductRead:
        product = await self._get_or_404(product_id)
        return ProductRead.model_validate(product)

    async def create_product(self, data: ProductCreate) -> ProductRead:
        vendor = await self.customer_repo.get_by_id(data.vendor_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
        if not vendor.is_vendor:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Customer is not a vendor",
            )
        product = await self.repo.create(data)
        return ProductRead.model_validate(product)

    async def update_product(
        self, product_id: uuid.UUID, data: ProductUpdate
    ) -> ProductRead:
        product = await self._get_or_404(product_id)

        if data.vendor_id is not None:
            vendor = await self.customer_repo.get_by_id(data.vendor_id)
            if not vendor:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
            if not vendor.is_vendor:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Customer is not a vendor",
                )

        product = await self.repo.update(product, data)
        return ProductRead.model_validate(product)

    async def delete_product(self, product_id: uuid.UUID) -> None:
        product = await self._get_or_404(product_id)
        await self.repo.delete(product)