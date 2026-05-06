import container
from drf_spectacular.utils import extend_schema
from interface.serializers.ai_serializer import RecommendInputSerializer, RecommendOutputSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class RecommendProductsView(APIView):

    @extend_schema(
        request=RecommendInputSerializer,
        responses={200: RecommendOutputSerializer},
        description="Recebe uma descrição do usuário e retorna produtos recomendados por IA.",
    )
    def post(self, request: Request) -> Response:
        serializer = RecommendInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data["query"].strip()
        try:
            result = container.recommend_products_uc.execute(query)
            return Response({"query": query, **result})
        except Exception as exc:
            return Response({"error": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
