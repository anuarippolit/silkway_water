import uuid 
from datetime import date, datetime
from sqlalchemy import Numeric, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.contact import Contact
from app.models.user import User
from app.enums import BottleCondition, PaymentStatus, OrderStatus

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    contact_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("contacts.id"))
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    bottles_qty: Mapped[int] = mapped_column()
    bottle_price: Mapped[float] = mapped_column(Numeric(10, 2))
    bottle_condition: Mapped[str] = mapped_column(String(20), default=BottleCondition.new)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    payment_status: Mapped[str] = mapped_column(String(20), default=PaymentStatus.unpaid)
    order_status: Mapped[str] = mapped_column(String(20), default=OrderStatus.actual)
    delivery_date: Mapped[date] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    addons: Mapped[list["OrderAddon"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    contact: Mapped["Contact"] = relationship(foreign_keys=[contact_id])
    created_by_user: Mapped["User"] = relationship(foreign_keys=[created_by])

class OrderAddon(Base):
    __tablename__ = "order_addons"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"))
    name: Mapped[str] = mapped_column(String(255))
    qty: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    order: Mapped["Order"] = relationship(back_populates="addons")