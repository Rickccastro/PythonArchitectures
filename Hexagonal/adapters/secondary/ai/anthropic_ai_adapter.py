import json
import os

from core.domain.ports.output.ai_recommendation_port import AIRecommendationPort

_KEYWORD_CATEGORIES: dict[str, list[str]] = {
    "eletrônicos": ["celular", "notebook", "tablet", "fone", "headphone", "câmera", "tv", "monitor"],
    "roupas": ["camisa", "calça", "vestido", "tênis", "sapato", "jaqueta", "blusa"],
    "alimentos": ["arroz", "feijão", "macarrão", "café", "chocolate", "biscoito", "suco"],
    "livros": ["livro", "romance", "técnico", "ficção", "história", "manual"],
    "esportes": ["bicicleta", "treino", "academia", "futebol", "corrida", "musculação"],
}


class AnthropicAIAdapter(AIRecommendationPort):
    def recommend(self, query: str) -> dict:
        api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if api_key:
            return self._recommend_via_api(query, api_key)
        return self._recommend_simulated(query)

    def _recommend_via_api(self, query: str, api_key: str) -> dict:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        prompt = (
            f'Dado a consulta "{query}", sugira produtos relevantes em português. '
            'Responda exclusivamente com JSON no formato: '
            '{"suggestions": ["produto1", "produto2", "produto3"], "reasoning": "motivo"}'
        )
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        result = json.loads(message.content[0].text)
        result["mode"] = "anthropic-api"
        return result

    def _recommend_simulated(self, query: str) -> dict:
        query_lower = query.lower()
        matched: list[str] = []
        for category, keywords in _KEYWORD_CATEGORIES.items():
            if any(kw in query_lower for kw in keywords) or category in query_lower:
                matched.append(category)

        if not matched:
            matched = ["eletrônicos", "roupas"]

        suggestions = [f"Produto popular em {cat}" for cat in matched[:3]]
        return {
            "suggestions": suggestions,
            "reasoning": f"Baseado em keywords detectadas na query: {query}",
            "mode": "simulated",
        }
