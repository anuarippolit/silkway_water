from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, or_, select
from app.models.contact import Contact
from app.models.order import Order
from app.schemas.contact import ContactUpdate
import uuid

async def get_all_contacts(db: AsyncSession) -> list[Contact]:
    result = await db.execute(select(Contact))
    return result.scalars().all()

async def search_contacts(db: AsyncSession, q: str) -> list[Contact]:
    result = await db.execute(select(Contact).where(or_(
    Contact.name.ilike(f"%{q}%"),
    Contact.phone.ilike(f"%{q}%"),
    Contact.address.ilike(f"%{q}%")
)))
    return result.scalars().all()

async def get_contact_by_id(db: AsyncSession, id: uuid.UUID) -> Contact | None:
    result = await db.execute(select(Contact).where(Contact.id == id))
    return result.scalars().first()

async def upsert_contact(db: AsyncSession, phone: str, address: str, name: str) -> Contact:
    result = await db.execute(select(Contact).where(Contact.phone == phone))
    contact = result.scalars().first()
    if contact:
        return contact 
    else:
        contact = Contact(phone=phone, address=address, name=name)
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        return contact


async def update_contact_stats(db: AsyncSession, id: uuid.UUID, bottles_qty: int) -> None:
    result = await db.execute(select(Contact).where(Contact.id == id))
    contact = result.scalars().first()
    if contact:
        contact.total_bottles += bottles_qty
        orders_count_result = await db.execute(select(func.count()).where(Order.contact_id == id))
        orders_count = orders_count_result.scalar()
        contact.avg_bottles = contact.total_bottles / orders_count if orders_count > 0 else 0
        await db.commit()
        await db.refresh(contact)

async def update_contact(db: AsyncSession, id: uuid.UUID, data: ContactUpdate) -> Contact:
    contact = await db.execute(select(Contact).where(Contact.id == id))
    contact = contact.scalars().first()
    if not contact: 
        return None 
    if data.name:
        contact.name = data.name
    if data.phone:
        contact.phone = data.phone
    if data.address:
        contact.address = data.address
    await db.commit()
    await db.refresh(contact)
    return contact 
