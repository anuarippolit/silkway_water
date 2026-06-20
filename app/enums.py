from enum import Enum

class BottleCondition(str, Enum):
    new = "new"
    medium = "medium"
    tired = "tired"
    pablo = "pablo"

class PaymentStatus(str, Enum):
    paid = "paid"
    unpaid = "unpaid"

class OrderStatus(str, Enum):
    actual = "actual"
    delivered = "delivered"
    cancelled = "cancelled"

class Role(str, Enum):
    admin="admin"
    courier="courier"