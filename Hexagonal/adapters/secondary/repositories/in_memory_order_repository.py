from core.domain.entities.order import Order
from core.domain.ports.output.order_repository_port import OrderRepositoryPort


class InMemoryOrderRepository(OrderRepositoryPort):
    def __init__(self) -> None:
        self._storage: dict[str, Order] = {}

    def save(self, order: Order) -> Order:
        self._storage[order.id] = order
        return order

    def find_by_id(self, order_id: str) -> Order | None:
        return self._storage.get(order_id)

    def find_all(self) -> list[Order]:
        return list(self._storage.values())
