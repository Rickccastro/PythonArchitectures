# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar o servidor de desenvolvimento
python manage.py runserver

# Rodar migrações (necessário apenas se adicionar Django models reais)
python manage.py migrate
```

Não há test runner configurado. Para adicionar testes, use `pytest` com `pytest-django`.

## Arquitetura

Este projeto segue **Clean Architecture** com quatro camadas com dependências unidirecionais estritas:

```
interface/ → application/ → domain/
infrastructure/            → domain/
interface/                 → infrastructure/ (somente via container.py)
```

### Camadas

**`domain/`** — zero dependências externas (apenas stdlib Python)
- `entities/` — dataclasses `Product` e `Order` (com `OrderStatus` enum)
- `repositories/` — ABCs `ProductRepository` e `OrderRepository` (contratos)
- `services/` — ABC `AIRecommendationService` (contrato do serviço de IA)

**`application/`** — importa apenas `domain/`
- `use_cases/products/` — `CreateProductUseCase`, `ListProductsUseCase`, `GetProductUseCase`
- `use_cases/orders/` — `CreateOrderUseCase` (decrementa estoque), `ListOrdersUseCase`
- `use_cases/ai/` — `RecommendProductsUseCase`

**`infrastructure/`** — implementações concretas, pode usar libs externas
- `repositories/` — `InMemoryProductRepository` e `InMemoryOrderRepository` (dicionários Python)
- `ai/` — `AIProductRecommendationService`: dual-mode — usa API real Anthropic se `ANTHROPIC_API_KEY` estiver definida, senão usa keyword matching simulado

**`interface/`** — controllers DRF
- `views/` — `ProductListView`, `ProductDetailView`, `OrderListView`, `RecommendProductsView`
- `serializers/` — validação de entrada e serialização de saída
- `urls.py` — rotas, incluídas em `config/urls.py` sob `/api/`

### Injeção de dependências

`container.py` (raiz do projeto) instancia todos os repositórios, o serviço de IA e os use cases como singletons na inicialização do processo. As views importam diretamente deste módulo (ex: `import container; container.list_products_uc.execute()`). Não há framework de DI — é Python puro.

### Persistência

Sem banco de dados real. Os repositórios em memória perdem todos os dados ao reiniciar o servidor. O `DATABASES` do Django aponta para SQLite `:memory:` apenas para satisfazer o framework — nenhuma model ORM é usada.

### Serviço de IA

`AIProductRecommendationService` detecta `ANTHROPIC_API_KEY` no ambiente:
- **Com chave**: chama `claude-haiku-4-5-20251001` e espera JSON com `{suggestions, reasoning}`
- **Sem chave**: executa keyword matching em português com categorias pré-definidas

Resposta sempre inclui o campo `mode: "anthropic-api" | "simulated"`.

## Endpoints

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/api/products/` | Lista produtos |
| POST | `/api/products/` | Cria produto |
| GET | `/api/products/<id>/` | Busca produto por ID |
| GET | `/api/orders/` | Lista pedidos |
| POST | `/api/orders/` | Cria pedido (valida estoque) |
| POST | `/api/ai/recommend/` | Recomendação por IA (`{"query": "..."}`) |

## Variáveis de ambiente

Copie `.env.example` para `.env`:

```
SECRET_KEY=...
ANTHROPIC_API_KEY=...   # opcional — sem isso o modo simulado é usado
```
