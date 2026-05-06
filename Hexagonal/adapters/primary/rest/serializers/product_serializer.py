from rest_framework import serializers


class ProductInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000, default="")
    price = serializers.FloatField(min_value=0.01)
    category = serializers.CharField(max_length=100)
    stock = serializers.IntegerField(min_value=0)


class ProductOutputSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    category = serializers.CharField()
    stock = serializers.IntegerField()
