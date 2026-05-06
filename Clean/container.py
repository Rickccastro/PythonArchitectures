"""
Container de Injeção de Dependências.

Instancia repositórios, serviços e use cases uma única vez (singletons).
As views importam deste módulo para obter os use cases prontos para uso.

Fluxo de dependência:
  infrastructure (repos + ai_service)
      ↓
  application (use cases recebem repos/services via construtor)
      ↓
  interface (views importam os use cases deste container)
"""
from infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.ai.ai_product_recommendation_service import AIProductRecommendationService

from application.use_cases.products.create_product import CreateProductUseCase
from application.use_cases.products.list_products import ListProductsUseCase
from application.use_cases.products.get_product import GetProductUseCase
from application.use_cases.orders.create_order import CreateOrderUseCase
from application.use_cases.orders.list_orders import ListOrdersUseCase
from application.use_cases.ai.recommend_products import RecommendProductsUseCase

# ---------- Repositórios em memória ----------
product_repo = InMemoryProductRepository()
order_repo = InMemoryOrderRepository()

# ---------- Serviço de IA ----------
ai_service = AIProductRecommendationService()

# ---------- Use Cases ----------
create_product_uc = CreateProductUseCase(product_repo)
list_products_uc = ListProductsUseCase(product_repo)
get_product_uc = GetProductUseCase(product_repo)

create_order_uc = CreateOrderUseCase(product_repo, order_repo)
list_orders_uc = ListOrdersUseCase(order_repo)

recommend_products_uc = RecommendProductsUseCase(product_repo, ai_service)
