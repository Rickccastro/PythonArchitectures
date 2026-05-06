from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    """Retorna todos os produtos disponíveis."""

    def __init__(self, product_repository: ProductRepository):
        self._repo = product_repository

    def execute(self) -> list[Product]:
        return self._repo.find_all()
