from rest_framework import serializers


class OrderInputSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)


class OrderOutputSerializer(serializers.Serializer):
    id = serializers.CharField()
    product_id = serializers.CharField()
    quantity = serializers.IntegerField()
    total_price = serializers.FloatField()
    # status é um Enum — source='status.value' acessa o atributo .value automaticamente
    status = serializers.CharField(source="status.value")
    created_at = serializers.DateTimeField()
