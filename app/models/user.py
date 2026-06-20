import uuid 
from datetime import datetime
from sqlalchemy import BigInteger, func, String
from sqlalchemy.orm import Mapped, mapped_column 
from app.core.database import Base 
from app.enums import Role


class User(Base):
    __tablename__="users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default = uuid.uuid4)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(20), default = Role.courier)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


