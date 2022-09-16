from django.db.models import Q
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from products.models import Product, Funding
from products.serializers import ProductListSerializer, \
                                 ProductCreateSerializer, \
                                 ProductDetailSerializer, \
                                 FundingSerializer
from products.permissions import ProductIsOwnerOrReadOnly, FundingIsOwner


class ProductViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action in ('funding_list', 'funding_create'):
            return Funding.objects.all()
        else:
            return Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'create':
            return ProductCreateSerializer
        elif self.action in ('funding_list', 'funding_create'):
            return FundingSerializer
        else:
            return ProductDetailSerializer

    def get_permissions(self):
        if self.action in ('funding_list', 'funding_create'):
            permission_classes = (FundingIsOwner,)
        else:
            permission_classes = (ProductIsOwnerOrReadOnly,)

        return [permission() for permission in permission_classes]

    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('name',)
    ordering_fields = ('created_at', 'total_fund',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 로그인된 사용자 정보를 추가해 Product 생성
            Product.objects.create(
                user_id=request.user.id,
                name=request.data['name'],
                description=request.data['description'],
                target_fund=request.data['target_fund'],
                fund_per_once=request.data['fund_per_once'],
                end_date=request.data['end_date'],
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def funding_list(self, request, pk):
        # 로그인된 사용자 본인의 펀딩 내역만 조회
        query = Q(product=pk) & Q(user=request.user)
        fundings = self.get_queryset().filter(query)

        serializer = self.get_serializer(fundings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def funding_create(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except:
            return Response({'message': '펀딩 상품이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # 로그인된 사용자 정보를 추가해 Funding 등록
                Funding.objects.create(
                    user_id=request.user.id,
                    product_id=pk,
                )

                # 해당 Product total_fund 수정
                fund_per_once = product.fund_per_once

                product.total_fund += fund_per_once
                product.save(update_fields=['total_fund'])

                return Response({'message': '펀딩에 성공하였습니다.'}, status=status.HTTP_201_CREATED)
