import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.order import OrderCreate, OrderRead
from app.services.order import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderRead])
async def list_orders(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await OrderService(db).list_orders()


@router.get("/customer/{customer_id}", response_model=list[OrderRead])
async def list_orders_by_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await OrderService(db).list_by_customer(customer_id)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await OrderService(db).get_order(order_id)


@router.post("/", response_model=OrderRead, status_code=201)
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await OrderService(db).create_order(data)


@router.delete("/{order_id}", status_code=204)
async def delete_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    await OrderService(db).delete_order(order_id)
