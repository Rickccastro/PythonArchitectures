# Entidade pura — representa um pedido de compra.
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Order:
    id: str
    product_id: str
    quantity: int
    total_price: float    # price * quantity, calculado no use case
    status: OrderStatus
    created_at: datetime
