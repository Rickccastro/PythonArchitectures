from domain.repositories.product_repository import ProductRepository
from domain.services.ai_recommendation_service import AIRecommendationService


class RecommendProductsUseCase:
    """
    Fluxo: Controller → UseCase → AIRecommendationService → retorna sugestões.
    O use case busca os produtos disponíveis e delega a lógica de IA ao serviço.
    """

    def __init__(self, product_repository: ProductRepository, ai_service: AIRecommendationService):
        self._product_repo = product_repository
        self._ai_service = ai_service

    def execute(self, query: str) -> dict:
        if not query.strip():
            raise ValueError("A query de busca não pode ser vazia.")

        products = self._product_repo.find_all()
        return self._ai_service.recommend(query, products)
