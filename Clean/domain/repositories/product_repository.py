# Interface (contrato) que qualquer repositório de produtos deve cumprir.
# A camada de domínio define o contrato; a infraestrutura implementa.
from abc import ABC, abstractmethod

from domain.entities.product import Product


class ProductRepository(ABC):

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Insere ou atualiza um produto."""
        ...

    @abstractmethod
    def find_by_id(self, product_id: str) -> Product | None:
        """Retorna produto pelo ID ou None se não existir."""
        ...

    @abstractmethod
    def find_all(self) -> list[Product]:
        """Retorna todos os produtos."""
        ...

    @abstractmethod
    def delete(self, product_id: str) -> bool:
        """Remove produto pelo ID. Retorna True se existia."""
        ...
