from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository


class GetProductUseCase:
    """Busca um produto específico pelo ID."""

    def __init__(self, product_repository: ProductRepository):
        self._repo = product_repository

    def execute(self, product_id: str) -> Product:
        product = self._repo.find_by_id(product_id)
        if product is None:
            raise ValueError(f"Produto '{product_id}' não encontrado.")
        return product
