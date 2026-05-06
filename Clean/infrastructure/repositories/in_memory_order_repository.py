from domain.entities.order import Order
from domain.repositories.order_repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):

    def __init__(self):
        self._storage: dict[str, Order] = {}

    def save(self, order: Order) -> Order:
        self._storage[order.id] = order
        return order

    def find_by_id(self, order_id: str) -> Order | None:
        return self._storage.get(order_id)

    def find_all(self) -> list[Order]:
        return list(self._storage.values())
