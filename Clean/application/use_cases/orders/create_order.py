import uuid
from datetime import datetime

from domain.entities.order import Order, OrderStatus
from domain.repositories.order_repository import OrderRepository
from domain.repositories.product_repository import ProductRepository


class CreateOrderUseCase:
    """
    Cria um pedido de compra.
    Regras de negócio:
    - Produto deve existir
    - Estoque deve ser suficiente
    - Stock é decrementado após o pedido
    """

    def __init__(self, product_repository: ProductRepository, order_repository: OrderRepository):
        self._product_repo = product_repository
        self._order_repo = order_repository

    def execute(self, product_id: str, quantity: int) -> Order:
        product = self._product_repo.find_by_id(product_id)
        if product is None:
            raise ValueError(f"Produto '{product_id}' não encontrado.")
        if quantity <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if product.stock < quantity:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {product.stock}, solicitado: {quantity}."
            )

        # Decrementa estoque
        product.stock -= quantity
        self._product_repo.save(product)

        order = Order(
            id=str(uuid.uuid4()),
            product_id=product_id,
            quantity=quantity,
            total_price=round(product.price * quantity, 2),
            status=OrderStatus.COMPLETED,
            created_at=datetime.now(),
        )
        return self._order_repo.save(order)
