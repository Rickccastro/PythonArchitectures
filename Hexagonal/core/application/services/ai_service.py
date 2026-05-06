from core.domain.ports.input.ai_service_port import AIServicePort
from core.domain.ports.output.ai_recommendation_port import AIRecommendationPort


class AIService(AIServicePort):
    def __init__(self, recommendation_port: AIRecommendationPort) -> None:
        self._port = recommendation_port

    def recommend_products(self, query: str) -> dict:
        if not query:
            raise ValueError("A query não pode ser vazia.")
        return self._port.recommend(query)
