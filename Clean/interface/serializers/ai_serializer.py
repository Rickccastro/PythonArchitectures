from rest_framework import serializers


class RecommendInputSerializer(serializers.Serializer):
    query = serializers.CharField(help_text="Descrição do que o usuário está procurando.")


class RecommendOutputSerializer(serializers.Serializer):
    query = serializers.CharField()
    suggestions = serializers.ListField(child=serializers.CharField())
    reasoning = serializers.CharField()
    mode = serializers.ChoiceField(choices=["simulated", "anthropic-api"])
