import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductHistoryRead,
    ProductRead,
    ProductUpdate,
)
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductRead])
async def list_products(
    include_inactive: bool = Query(default=False),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Return products; inactive products are excluded unless include_inactive=true."""
    return await ProductService(db).list_products(include_inactive=include_inactive)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Return a single product by ID, or 404 if not found."""
    return await ProductService(db).get_product(product_id)


@router.get("/{product_id}/history", response_model=list[ProductHistoryRead])
async def get_product_history(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Return the full audit history for a product, newest entry first."""
    return await ProductService(db).get_history(product_id)


@router.post("/", response_model=ProductRead, status_code=201)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Create a new active product."""
    return await ProductService(db).create_product(data)


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a product's fields and record the change in history; returns 409 if inactive."""
    return await ProductService(db).update_product(product_id, data, current_user.id)


@router.post("/{product_id}/deactivate", response_model=ProductRead)
async def deactivate_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft-delete a product; returns 409 if already inactive."""
    return await ProductService(db).deactivate_product(product_id, current_user.id)


@router.post("/{product_id}/restore", response_model=ProductRead)
async def restore_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Restore a deactivated product; returns 409 if already active."""
    return await ProductService(db).restore_product(product_id, current_user.id)
