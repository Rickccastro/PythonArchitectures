from abc import ABC, abstractmethod

from core.domain.entities.order import Order


class OrderRepositoryPort(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order: ...

    @abstractmethod
    def find_by_id(self, order_id: str) -> Order | None: ...

    @abstractmethod
    def find_all(self) -> list[Order]: ...
