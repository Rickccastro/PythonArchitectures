from abc import ABC, abstractmethod

from core.domain.entities.product import Product


class ProductRepositoryPort(ABC):
    @abstractmethod
    def save(self, product: Product) -> Product: ...

    @abstractmethod
    def find_by_id(self, product_id: str) -> Product | None: ...

    @abstractmethod
    def find_all(self) -> list[Product]: ...

    @abstractmethod
    def delete(self, product_id: str) -> bool: ...
