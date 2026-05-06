import container
from adapters.primary.rest.serializers.product_serializer import ProductInputSerializer, ProductOutputSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProductListView(APIView):
    @extend_schema(responses=ProductOutputSerializer(many=True))
    def get(self, request: Request) -> Response:
        products = container.product_service.list_all()
        return Response(ProductOutputSerializer(products, many=True).data)

    @extend_schema(request=ProductInputSerializer, responses={201: ProductOutputSerializer})
    def post(self, request: Request) -> Response:
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product = container.product_service.create(**serializer.validated_data)
            return Response(ProductOutputSerializer(product).data, status=status.HTTP_201_CREATED)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    @extend_schema(responses=ProductOutputSerializer)
    def get(self, request: Request, product_id: str) -> Response:
        product = container.product_service.get_by_id(product_id)
        if product is None:
            return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductOutputSerializer(product).data)
