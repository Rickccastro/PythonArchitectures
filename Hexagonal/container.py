# Composição raiz — instancia adapters secundários, injeta nos serviços do core.
# Views importam daqui; o core nunca conhece este módulo.
from adapters.secondary.ai.anthropic_ai_adapter import AnthropicAIAdapter
from adapters.secondary.repositories.in_memory_order_repository import InMemoryOrderRepository
from adapters.secondary.repositories.in_memory_product_repository import InMemoryProductRepository
from core.application.services.ai_service import AIService
from core.application.services.order_service import OrderService
from core.application.services.product_service import ProductService

# Secondary adapters (driven side)
_product_repo = InMemoryProductRepository()
_order_repo = InMemoryOrderRepository()
_ai_adapter = AnthropicAIAdapter()

# Application services (core — implements input ports, depends on output ports)
product_service = ProductService(repository=_product_repo)
order_service = OrderService(product_repo=_product_repo, order_repo=_order_repo)
ai_service = AIService(recommendation_port=_ai_adapter)
