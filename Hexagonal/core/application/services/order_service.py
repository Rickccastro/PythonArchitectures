import uuid
from datetime import datetime

from core.domain.entities.order import Order, OrderStatus
from core.domain.ports.input.order_service_port import OrderServicePort
from core.domain.ports.output.order_repository_port import OrderRepositoryPort
from core.domain.ports.output.product_repository_port import ProductRepositoryPort


class OrderService(OrderServicePort):
    def __init__(self, product_repo: ProductRepositoryPort, order_repo: OrderRepositoryPort) -> None:
        self._product_repo = product_repo
        self._order_repo = order_repo

    def create(self, product_id: str, quantity: int) -> Order:
        product = self._product_repo.find_by_id(product_id)
        if product is None:
            raise ValueError("Produto não encontrado.")
        if quantity <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if product.stock < quantity:
            raise ValueError("Estoque insuficiente.")

        product.stock -= quantity
        self._product_repo.save(product)

        order = Order(
            id=str(uuid.uuid4()),
            product_id=product_id,
            quantity=quantity,
            total_price=product.price * quantity,
            status=OrderStatus.COMPLETED,
            created_at=datetime.now(),
        )
        return self._order_repo.save(order)

    def list_all(self) -> list[Order]:
        return self._order_repo.find_all()
