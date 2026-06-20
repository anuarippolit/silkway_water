from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.order import OrderCreate, OrderUpdate, OrderStatusPatch
from app.models.order import Order, OrderAddon
from app.services.contact_service import update_contact_stats, upsert_contact
from datetime import date
import uuid
from sqlalchemy.orm import selectinload

async def create_order(db: AsyncSession, data: OrderCreate, created_by: uuid.UUID) -> Order:
    contact = await upsert_contact(db, data.phone, data.address, data.name)

    order = Order(
        contact_id=contact.id,
        bottles_qty=data.bottles_qty,
        bottle_price=data.bottle_price,
        bottle_condition=data.bottle_condition,
        payment_status=data.payment_status,
        order_status=data.order_status,
        delivery_date=data.delivery_date,
        created_by=created_by,
        addons=[OrderAddon(name=addon.name, qty=addon.qty, price=addon.price) for addon in data.addons]
    )
    order.total_amount = order.bottles_qty * order.bottle_price + sum(addon.qty * addon.price for addon in order.addons)

    db.add(order)
    await db.commit()
    await update_contact_stats(db, contact.id, data.bottles_qty)

    result = await db.execute(
        select(Order)
        .where(Order.id == order.id)
        .options( # it's relations
            selectinload(Order.contact),
            selectinload(Order.created_by_user),
            selectinload(Order.addons)
        )
    )
    return result.scalars().first()

async def get_orders(db: AsyncSession, delivery_date: date = None, status: str = None) -> list[Order]:
    query = (
        select(Order)
        .options(
            selectinload(Order.contact),
            selectinload(Order.addons)
        )
    )
    if delivery_date:
        query = query.where(Order.delivery_date == delivery_date)
    if status:
        query = query.where(Order.order_status == status)
    orders = await db.execute(query)
    return orders.scalars().all()

async def get_order_by_id(db: AsyncSession, order_id: uuid.UUID) -> Order | None:
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.contact),
            selectinload(Order.addons)
        )
    )
    return result.scalars().first()

async def update_order(db: AsyncSession, order_id: uuid.UUID, data: OrderUpdate) -> Order:
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.contact),
            selectinload(Order.addons)
        )
    )
    order = result.scalars().first()
    if not order:
        return None
    
    if data.contact_id:
        order.contact_id = data.contact_id
    if data.bottles_qty:
        order.bottles_qty = data.bottles_qty
        await update_contact_stats(db, order.contact_id, data.bottles_qty)
    if data.bottle_price:
        order.bottle_price = data.bottle_price
    if data.bottle_condition:
        order.bottle_condition = data.bottle_condition
    if data.payment_status:
        order.payment_status = data.payment_status
    if data.order_status:
        order.order_status = data.order_status
    if data.delivery_date:
        order.delivery_date = data.delivery_date

    order.total_amount = order.bottles_qty * order.bottle_price + sum(addon.qty * addon.price for addon in order.addons)

    await db.commit()
    await db.refresh(order)
    return order

async def update_order_status(db: AsyncSession, order_id: uuid.UUID, data: OrderStatusPatch) -> Order:
    order = await db.execute(select(Order).where(Order.id == order_id))
    order = order.scalars().first()
    if not order:
        return None 
    else: 
        order.order_status = data.order_status
        await db.commit()
        await db.refresh(order)
        return order

async def delete_order(db: AsyncSession, order_id: uuid.UUID) -> None:
    order = await db.execute(select(Order).where(Order.id == order_id))
    order = order.scalars().first()
    if order:
        await db.delete(order)
        await db.commit()
    return None