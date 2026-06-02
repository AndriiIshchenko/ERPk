import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.order import OrderCreate, OrderItemAdd, OrderRead
from app.services.order import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderRead])
async def list_orders(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Return all orders."""
    return await OrderService(db).list_orders()


@router.get("/customer/{customer_id}", response_model=list[OrderRead])
async def list_orders_by_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Return all orders belonging to a specific customer."""
    return await OrderService(db).list_by_customer(customer_id)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Return a single order by ID, or 404 if not found."""
    return await OrderService(db).get_order(order_id)


@router.post("/", response_model=OrderRead, status_code=201)
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Create an empty draft order for an existing customer."""
    return await OrderService(db).create_order(data)


@router.post("/{order_id}/items", response_model=OrderRead)
async def add_item(
    order_id: uuid.UUID,
    data: OrderItemAdd,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Add a product to a draft order; returns 409 if already present or order is not draft."""
    return await OrderService(db).add_item(order_id, data.product_id)


@router.delete("/{order_id}/items/{item_id}", response_model=OrderRead)
async def remove_item(
    order_id: uuid.UUID,
    item_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Remove a line item from a draft order."""
    return await OrderService(db).remove_item(order_id, item_id)


@router.post("/{order_id}/pay", response_model=OrderRead)
async def mark_paid(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Transition a pending order to paid status."""
    return await OrderService(db).mark_paid(order_id)


@router.post("/{order_id}/confirm", response_model=OrderRead)
async def confirm_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Confirm a draft order (moves to pending); requires at least one item."""
    return await OrderService(db).confirm_order(order_id)


@router.post("/{order_id}/cancel", response_model=OrderRead)
async def cancel_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Cancel a draft or pending order."""
    return await OrderService(db).cancel_order(order_id)


@router.delete("/{order_id}", status_code=204)
async def delete_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Hard-delete an order and all its items."""
    await OrderService(db).delete_order(order_id)
