from django.urls import path

from interface.views.ai_views import RecommendProductsView
from interface.views.order_views import OrderListView
from interface.views.product_views import ProductDetailView, ProductListView

urlpatterns = [
    # Produtos
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<str:product_id>/", ProductDetailView.as_view(), name="product-detail"),
    # Pedidos
    path("orders/", OrderListView.as_view(), name="order-list"),
    # IA
    path("ai/recommend/", RecommendProductsView.as_view(), name="ai-recommend"),
]
