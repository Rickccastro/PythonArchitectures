import uuid

from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository


class CreateProductUseCase:
    """Valida os dados e persiste um novo produto."""

    def __init__(self, product_repository: ProductRepository):
        self._repo = product_repository

    def execute(self, name: str, description: str, price: float, category: str, stock: int) -> Product:
        if price <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        if stock < 0:
            raise ValueError("O estoque não pode ser negativo.")
        if not name.strip():
            raise ValueError("O nome do produto é obrigatório.")

        product = Product(
            id=str(uuid.uuid4()),
            name=name.strip(),
            description=description,
            price=price,
            category=category,
            stock=stock,
        )
        return self._repo.save(product)
