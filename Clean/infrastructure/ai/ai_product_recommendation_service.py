"""
AIProductRecommendationService — Dual-mode:
  - Se ANTHROPIC_API_KEY estiver configurada: chama a API real do Claude.
  - Caso contrário: usa um algoritmo simples de palavras-chave (simulado).

Implementa AIRecommendationService (contrato definido no domain).
"""
import json
import os

from domain.entities.product import Product
from domain.services.ai_recommendation_service import AIRecommendationService


class AIProductRecommendationService(AIRecommendationService):

    def __init__(self):
        self._api_key = os.getenv("ANTHROPIC_API_KEY")

    def recommend(self, query: str, products: list[Product]) -> dict:
        if self._api_key:
            return self._real_recommendation(query, products)
        return self._simulated_recommendation(query, products)

    # ------------------------------------------------------------------
    # Modo real: chama a API da Anthropic
    # ------------------------------------------------------------------

    def _real_recommendation(self, query: str, products: list[Product]) -> dict:
        import anthropic  # importado aqui para não quebrar se a lib não estiver instalada

        product_list = "\n".join(
            f"- {p.name} (categoria: {p.category}): {p.description} — R${p.price:.2f}, estoque: {p.stock}"
            for p in products
        )
        if not product_list:
            product_list = "(nenhum produto cadastrado ainda)"

        prompt = f"""Você é um assistente especialista em recomendação de produtos de uma loja online.

Produtos disponíveis no catálogo:
{product_list}

O cliente digitou: "{query}"

Analise o interesse do cliente e recomende os produtos mais relevantes do catálogo acima.
Responda SOMENTE com um JSON válido no seguinte formato (sem markdown, sem texto fora do JSON):
{{
  "suggestions": ["Nome do Produto 1", "Nome do Produto 2"],
  "reasoning": "Explicação em português do por quê desses produtos"
}}"""

        client = anthropic.Anthropic(api_key=self._api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = message.content[0].text.strip()
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            # Se o modelo não retornou JSON puro, usa o texto como reasoning
            result = {"suggestions": [], "reasoning": raw}

        result["mode"] = "anthropic-api"
        return result

    # ------------------------------------------------------------------
    # Modo simulado: matching por palavras-chave (sem API externa)
    # ------------------------------------------------------------------

    def _simulated_recommendation(self, query: str, products: list[Product]) -> dict:
        # Mapa de categorias de interesse → termos relacionados
        _INTEREST_KEYWORDS: dict[str, list[str]] = {
            "programação": ["programação", "código", "software", "desenvolvimento", "python", "javascript", "tecnologia"],
            "estudo": ["estudo", "aprender", "aprendizado", "curso", "livro", "leitura", "educação"],
            "fitness": ["fitness", "exercício", "academia", "treino", "musculação", "saúde", "esporte"],
            "cozinha": ["cozinha", "culinária", "receita", "comida", "gastronomia", "chef"],
            "games": ["game", "jogo", "gamer", "gaming", "videogame", "console"],
            "música": ["música", "instrumento", "guitarra", "piano", "tocar"],
        }

        query_lower = query.lower()
        scores: list[tuple[int, Product]] = []

        for product in products:
            if product.stock == 0:
                continue  # ignora produtos sem estoque

            score = 0
            product_text = f"{product.name} {product.description} {product.category}".lower()

            # Palavra da query aparece diretamente no produto
            for word in query_lower.split():
                if len(word) > 2 and word in product_text:
                    score += 2

            # Correspondência por categoria de interesse
            for _, keywords in _INTEREST_KEYWORDS.items():
                query_matches = any(k in query_lower for k in keywords)
                product_matches = any(k in product_text for k in keywords)
                if query_matches and product_matches:
                    score += 3

            if score > 0:
                scores.append((score, product))

        scores.sort(key=lambda x: x[0], reverse=True)
        top = scores[:3]

        if top:
            suggestions = [p.name for _, p in top]
            reasoning = (
                f"Com base na sua busca por '{query}', identifiquei estes produtos como mais relevantes "
                f"para o seu interesse."
            )
        elif products:
            # Fallback: sugere os primeiros produtos com estoque
            available = [p for p in products if p.stock > 0][:2]
            suggestions = [p.name for p in available]
            reasoning = (
                f"Não encontrei produtos específicos para '{query}'. "
                f"Aqui estão alguns produtos populares do nosso catálogo."
            )
        else:
            suggestions = []
            reasoning = "Ainda não temos produtos cadastrados. Volte em breve!"

        return {
            "suggestions": suggestions,
            "reasoning": reasoning,
            "mode": "simulated",
        }
