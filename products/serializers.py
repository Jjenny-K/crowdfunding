from rest_framework import serializers

from products.models import Product, Funding


class ProductSerializer(serializers.ModelSerializer):
    """ 상품 serializer """
    user_name = serializers.CharField(source='user')

    class Meta:
        model = Product
        fields = (
            'user_name',
            'name',
            'description',
            'target_fund',
            'fund_per_once',
            'total_fund',
            'end_date',
        )
        extra_kwargs = {
            'total_fund': {'write_only': True}
        }
