import uuid

from core.domain.entities.product import Product
from core.domain.ports.input.product_service_port import ProductServicePort
from core.domain.ports.output.product_repository_port import ProductRepositoryPort


class ProductService(ProductServicePort):
    def __init__(self, repository: ProductRepositoryPort) -> None:
        self._repo = repository

    def create(self, name: str, description: str, price: float, category: str, stock: int) -> Product:
        if not name:
            raise ValueError("O nome do produto é obrigatório.")
        if price <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        if stock < 0:
            raise ValueError("O estoque não pode ser negativo.")

        product = Product(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            price=price,
            category=category,
            stock=stock,
        )
        return self._repo.save(product)

    def list_all(self) -> list[Product]:
        return self._repo.find_all()

    def get_by_id(self, product_id: str) -> Product | None:
        return self._repo.find_by_id(product_id)
