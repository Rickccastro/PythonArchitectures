import container
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class RecommendProductsView(APIView):
    @extend_schema(
        request={"application/json": {"type": "object", "properties": {"query": {"type": "string"}}}},
        responses={200: {"type": "object"}},
    )
    def post(self, request: Request) -> Response:
        query = request.data.get("query", "")
        try:
            result = container.ai_service.recommend_products(query)
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
