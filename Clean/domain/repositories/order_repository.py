from abc import ABC, abstractmethod

from domain.entities.order import Order


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: Order) -> Order:
        """Persiste um pedido."""
        ...

    @abstractmethod
    def find_by_id(self, order_id: str) -> Order | None:
        ...

    @abstractmethod
    def find_all(self) -> list[Order]:
        ...
