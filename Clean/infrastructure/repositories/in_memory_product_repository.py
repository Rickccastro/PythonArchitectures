# Implementação em memória — usa um dicionário Python como "banco de dados".
# Implementa a interface ProductRepository definida no domain.
from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):

    def __init__(self):
        # dict[id, Product] — persiste enquanto o processo estiver rodando
        self._storage: dict[str, Product] = {}

    def save(self, product: Product) -> Product:
        self._storage[product.id] = product
        return product

    def find_by_id(self, product_id: str) -> Product | None:
        return self._storage.get(product_id)

    def find_all(self) -> list[Product]:
        return list(self._storage.values())

    def delete(self, product_id: str) -> bool:
        if product_id in self._storage:
            del self._storage[product_id]
            return True
        return False
