import uuid 
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from app.enums import BottleCondition, PaymentStatus, OrderStatus
from typing import Optional
from app.schemas.contact import ContactShort
from app.schemas.user import UserResponse

class OrderAddonCreate(BaseModel):
    name: str
    qty: int
    price: float

class OrderAddonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    qty: int
    price: float

class OrderCreate(BaseModel):
    phone: str
    address: str
    name: str
    bottles_qty: int
    bottle_price: float
    bottle_condition: BottleCondition
    payment_status: PaymentStatus
    order_status: OrderStatus
    delivery_date: date
    addons: list[OrderAddonCreate] = []

class OrderUpdate(BaseModel):
    contact_id: Optional[uuid.UUID] = None
    bottles_qty: Optional[int] = None
    bottle_price: Optional[float] = None
    bottle_condition: Optional[BottleCondition] = None
    payment_status: Optional[PaymentStatus] = None
    order_status: Optional[OrderStatus] = None
    delivery_date: Optional[date] = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    contact: ContactShort
    created_by: uuid.UUID
    bottles_qty: int
    bottle_price: float
    bottle_condition: BottleCondition
    payment_status: PaymentStatus
    order_status: OrderStatus
    delivery_date: date
    total_amount: float
    created_at: datetime
    updated_at: datetime
    addons: list[OrderAddonResponse]

class OrderStatusPatch(BaseModel):
    order_status: OrderStatus