from django.db.models import Q
from rest_framework import generics, status, filters
from rest_framework.response import Response

from products.models import Product, Funding
from products.serializers import ProductListSerializer, \
                                 ProductCreateSerializer, \
                                 ProductDetailSerializer, \
                                 FundingSerializer
from products.permissions import ProductIsOwnerOrReadOnly, FundingIsOwner


class ProductListViews(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = (ProductIsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        elif self.request.method == 'POST':
            return ProductCreateSerializer

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


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = (ProductIsOwnerOrReadOnly,)


class ProductFundingView(generics.ListCreateAPIView):
    queryset = Funding.objects.all()
    serializer_class = FundingSerializer
    permission_classes = (FundingIsOwner,)

    def list(self, request, pk, *args, **kwargs):
        # 로그인된 사용자 본인의 펀딩 내역만 조회
        query = Q(product=pk) & Q(user=request.user)
        self.queryset = self.queryset.filter(query)

        return super().list(request, *args, **kwargs)

    def create(self, request, pk, *args, **kwargs):
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
