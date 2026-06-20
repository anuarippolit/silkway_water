import uuid 
from datetime import datetime
from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Contact(Base):
    __tablename__="contacts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default = uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(20), unique=True)
    avg_bottles: Mapped[int] = mapped_column(default=0)
    total_bottles: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    
