import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# used in Order create logic. If we put data of user that does not exist, we use this to create it. 

class ContactCreate(BaseModel):
    name: str
    address: str
    phone: str

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class ContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    address: str
    phone: str
    avg_bottles: float 
    total_bottles: int
    created_at: datetime
    updated_at: datetime

# in order Response 

class ContactShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    address: str
    phone: str
