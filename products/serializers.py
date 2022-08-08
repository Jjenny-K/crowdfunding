from rest_framework import serializers

from products.models import Product, Funding


class ProductSerializer(serializers.ModelSerializer):
    """ 상품 serializer """
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'total_fund': {'write_only': True}
        }
