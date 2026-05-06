import container
from drf_spectacular.utils import extend_schema
from interface.serializers.product_serializer import ProductInputSerializer, ProductOutputSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProductListView(APIView):

    @extend_schema(responses=ProductOutputSerializer(many=True))
    def get(self, request: Request) -> Response:
        products = container.list_products_uc.execute()
        return Response(ProductOutputSerializer(products, many=True).data)

    @extend_schema(request=ProductInputSerializer, responses={201: ProductOutputSerializer})
    def post(self, request: Request) -> Response:
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product = container.create_product_uc.execute(**serializer.validated_data)
            return Response(ProductOutputSerializer(product).data, status=status.HTTP_201_CREATED)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):

    @extend_schema(responses={200: ProductOutputSerializer, 404: None})
    def get(self, request: Request, product_id: str) -> Response:
        try:
            product = container.get_product_uc.execute(product_id)
            return Response(ProductOutputSerializer(product).data)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
