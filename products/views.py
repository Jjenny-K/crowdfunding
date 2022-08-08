from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response

from products.models import Product, Funding
from products.serializers import ProductSerializer


class ProductListViews(views.APIView):
    def get_list(self):
        return get_list_or_404(Product)

    def get(self, request):
        """ GET api/products """
        products = self.get_list()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ POST api/products """
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=self.request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(views.APIView):
    def get_object(self, pk):
        return get_object_or_404(Product, id=pk)

    def get(self, request, pk):
        """ GET api/products/:pk """
        product = self.get_object(pk)
        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """ PUT api/products/:pk """
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        product = self.get_object(pk)

        if product is not None:
            product.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
