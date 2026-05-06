# Contrato do serviço de IA — definido no domain para que application possa
# depender da interface sem conhecer a implementação concreta (infrastructure).
from abc import ABC, abstractmethod

from domain.entities.product import Product


class AIRecommendationService(ABC):

    @abstractmethod
    def recommend(self, query: str, products: list[Product]) -> dict:
        """
        Recebe a query do usuário e a lista de produtos disponíveis.
        Retorna dict com: suggestions (list[str]), reasoning (str), mode (str).
        """
        ...
