from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Order:
    id: str
    product_id: str
    quantity: int
    total_price: float  # calculado no serviço: price * quantity
    status: OrderStatus
    created_at: datetime
