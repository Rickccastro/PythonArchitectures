from abc import ABC, abstractmethod


class AIServicePort(ABC):
    @abstractmethod
    def recommend_products(self, query: str) -> dict: ...
