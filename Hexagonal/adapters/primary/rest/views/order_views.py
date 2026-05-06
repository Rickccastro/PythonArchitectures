import container
from adapters.primary.rest.serializers.order_serializer import OrderInputSerializer, OrderOutputSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class OrderListView(APIView):
    @extend_schema(responses=OrderOutputSerializer(many=True))
    def get(self, request: Request) -> Response:
        orders = container.order_service.list_all()
        return Response(OrderOutputSerializer(orders, many=True).data)

    @extend_schema(request=OrderInputSerializer, responses={201: OrderOutputSerializer})
    def post(self, request: Request) -> Response:
        serializer = OrderInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order = container.order_service.create(**serializer.validated_data)
            return Response(OrderOutputSerializer(order).data, status=status.HTTP_201_CREATED)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
