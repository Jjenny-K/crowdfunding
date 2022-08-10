from rest_framework import serializers

from products.models import Product, Funding


class ProductListSerializer(serializers.ModelSerializer):
    """ 상품 목록 serializer """
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Product
        fields = (
            'name',
            'user_name',
            'total_fund',
            'achievement_rate',
            'd_day',
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    """ 상품 등록 serializer """
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'target_fund',
            'fund_per_once',
            'end_date',
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    """ 상품 상세 serializer """
    user_name = serializers.ReadOnlyField(source='user.username')
    participants = serializers.SerializerMethodField('get_participants')

    class Meta:
        model = Product
        fields = (
            'name',
            'user_name',
            'description',
            'target_fund',
            'fund_per_once',
            'end_date',
            'total_fund',
            'achievement_rate',
            'd_day',
            'participants',
        )
        read_only_fields = (
            'target_fund',
            'total_fund',
            'achievement_rate',
            'd_day',
            'participants',
        )

    def get_participants(self, obj):
        return Funding.objects.filter(product_id=obj.id).count()
