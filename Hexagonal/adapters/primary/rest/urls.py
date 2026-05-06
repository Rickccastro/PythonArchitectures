from adapters.primary.rest.views.ai_views import RecommendProductsView
from adapters.primary.rest.views.order_views import OrderListView
from adapters.primary.rest.views.product_views import ProductDetailView, ProductListView
from django.urls import path

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<str:product_id>/", ProductDetailView.as_view(), name="product-detail"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("ai/recommend/", RecommendProductsView.as_view(), name="ai-recommend"),
]
