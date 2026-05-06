from abc import ABC, abstractmethod

from core.domain.entities.order import Order


class OrderServicePort(ABC):
    @abstractmethod
    def create(self, product_id: str, quantity: int) -> Order: ...

    @abstractmethod
    def list_all(self) -> list[Order]: ...
