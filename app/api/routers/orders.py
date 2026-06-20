from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.order import OrderResponse, OrderCreate, OrderUpdate, OrderStatusPatch
from app.services import order_service
from app.dependencies import get_current_user, require_admin
from app.models.user import User
import uuid
from datetime import date

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/")
async def get_all_orders(date: date = None, status: str = None, db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)) -> list[OrderResponse]:
    return await order_service.get_orders(db, date, status)


@router.get("/{id}")
async def get_order(id: uuid.UUID, db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)) -> OrderResponse:
    order = await order_service.get_order_by_id(db, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/")
async def create_order(data: OrderCreate, db: AsyncSession = Depends(get_db), user: User = Depends(require_admin)) -> OrderResponse:
    return await order_service.create_order(db, data, user.id)

@router.patch("/{id}")
async def update_order(id: uuid.UUID, data: OrderUpdate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)) -> OrderResponse:
    order = await order_service.update_order(db, id, data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{id}/status")
async def update_order_status(id: uuid.UUID, data: OrderStatusPatch, db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    order = await order_service.update_order_status(db, id, data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{id}")
async def delete_order(id: uuid.UUID, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)) -> None:
    order = await order_service.get_order_by_id(db, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await order_service.delete_order(db, id)