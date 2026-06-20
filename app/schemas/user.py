from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime

from app.enums import Role

class UserCreate(BaseModel):
    telegram_id: int
    name: str
    role: Role 

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    telegram_id: int
    name: str
    role: Role
    created_at: datetime 