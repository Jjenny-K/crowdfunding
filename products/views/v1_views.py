from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import views, status
from rest_framework.response import Response

from products.models import Product, Funding
from products.serializers import ProductListSerializer, \
                                 ProductCreateSerializer, \
                                 ProductDetailSerializer, \
                                 FundingSerializer
from products.utils import RequestHandler
from products.permissions import ProductIsOwnerOrReadOnly, FundingIsOwner


class ProductListViews(views.APIView, RequestHandler):
    permission_classes = (ProductIsOwnerOrReadOnly,)

    def get(self, request):
        """ GET api/products """
        query = Q()
        search, sort = self._request_param(request)

        if search:
            # 파라미터 중 search가 있을 때, 상품명 like 검색
            query &= Q(name__icontains=search)

        products = Product.objects.filter(query)

        if sort:
            # 파라미터 중 sort가 있을 때, 상품 목록 정렬
            products = products.order_by(sort)

        serializer = ProductListSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ POST api/products """
        serializer = ProductCreateSerializer(data=request.data)

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


class ProductDetailView(views.APIView):
    permission_classes = (ProductIsOwnerOrReadOnly,)

    def get_object(self, pk):
        return get_object_or_404(Product, id=pk)

    def get(self, request, pk):
        """ GET api/products/:pk """
        product = self.get_object(pk)
        serializer = ProductDetailSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """ PUT api/products/:pk """
        product = self.get_object(pk)
        serializer = ProductDetailSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """ DELETE api/products/:pk """
        product = self.get_object(pk)

        if product is not None:
            product.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductFundingView(views.APIView):
    permission_classes = (FundingIsOwner,)
    
    def get_product(self, pk):
        return get_object_or_404(Product, id=pk)

    def get(self, request, pk):
        """ GET api/product/:pk/funding """

        # pk 값과 맞는 product object 조회
        product = self.get_object(pk)

        # 로그인된 사용자 본인의 펀딩 내역만 조회
        query = Q(product=pk) & Q(user=request.user)
        fundings = Funding.objects.filter(query)

        serializer = FundingSerializer(fundings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """ POST api/product/:pk/funding """
        # pk 값과 맞는 product object 조회
        product = self.get_product(pk)

        serializer = FundingSerializer(data=request.data)

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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
