from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date"]


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Product.objects.all(),
        source="products",
        required=False,
    )
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "products",
            "product_ids",
            "supplier",
            "debt",
            "created_at",
            "level",
        ]
        read_only_fields = ["created_at", "level"]

    def update(self, instance, validated_data):
        # запрет менять долг через API
        validated_data.pop("debt", None)
        return super().update(instance, validated_data)
