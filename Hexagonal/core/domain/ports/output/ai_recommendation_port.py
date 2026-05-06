from abc import ABC, abstractmethod


class AIRecommendationPort(ABC):
    @abstractmethod
    def recommend(self, query: str) -> dict: ...
