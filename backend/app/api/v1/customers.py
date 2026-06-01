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
    is_vendor: bool | None = None,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await CustomerService(db).list_customers(is_vendor=is_vendor)


@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await CustomerService(db).get_customer(customer_id)


@router.post("/", response_model=CustomerRead, status_code=201)
async def create_customer(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await CustomerService(db).create_customer(data)


@router.put("/{customer_id}", response_model=CustomerRead)
async def update_customer(
    customer_id: uuid.UUID,
    data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await CustomerService(db).update_customer(customer_id, data)


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    await CustomerService(db).delete_customer(customer_id)
