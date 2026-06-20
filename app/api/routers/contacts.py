from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.services import contact_service
from app.core.database import get_db
from app.schemas.contact import ContactResponse, ContactUpdate
from app.dependencies import require_admin
from app.models.user import User

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("/")
async def get_contacts(db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)) -> list[ContactResponse]:
    return await contact_service.get_all_contacts(db)
    

@router.get("/search")
async def contact_search(q: str, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)) -> list[ContactResponse]:
    return await contact_service.search_contacts(db, q)

@router.get("/{id}")
async def get_contact_id(id: uuid.UUID, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)) -> ContactResponse:
    contact = await contact_service.get_contact_by_id(db, id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.patch("/{id}")
async def update_contact(id: uuid.UUID, data: ContactUpdate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)) -> ContactResponse:
    contact =  await contact_service.update_contact(db, id, data)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact