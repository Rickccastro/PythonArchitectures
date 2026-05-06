from abc import ABC, abstractmethod

from core.domain.entities.product import Product


class ProductServicePort(ABC):
    @abstractmethod
    def create(self, name: str, description: str, price: float, category: str, stock: int) -> Product: ...

    @abstractmethod
    def list_all(self) -> list[Product]: ...

    @abstractmethod
    def get_by_id(self, product_id: str) -> Product | None: ...
