from domain.entities.order import Order
from domain.repositories.order_repository import OrderRepository


class ListOrdersUseCase:
    """Retorna todos os pedidos registrados."""

    def __init__(self, order_repository: OrderRepository):
        self._repo = order_repository

    def execute(self) -> list[Order]:
        return self._repo.find_all()
