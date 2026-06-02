import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.services.customer import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=list[CustomerRead])
async def list_customers(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Return all customers."""
    return await CustomerService(db).list_customers()


@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Return a single customer by ID, or 404 if not found."""
    return await CustomerService(db).get_customer(customer_id)


@router.post("/", response_model=CustomerRead, status_code=201)
async def create_customer(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Create a new customer; returns 409 if the email is already registered."""
    return await CustomerService(db).create_customer(data)


@router.put("/{customer_id}", response_model=CustomerRead)
async def update_customer(
    customer_id: uuid.UUID,
    data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Update a customer's fields; returns 409 on duplicate email."""
    return await CustomerService(db).update_customer(customer_id, data)


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    """Hard-delete a customer by ID."""
    await CustomerService(db).delete_customer(customer_id)
