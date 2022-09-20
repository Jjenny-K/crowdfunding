from django.urls import path

from products.views import ProductViewSet

product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

product_funding = ProductViewSet.as_view({
    'get': 'funding_list',
    'post': 'funding_create',
})

urlpatterns = [
    path('products', product_list, name='product-list'),
    path('products/<int:pk>', product_detail, name='product-detail'),
    path('products/<int:pk>/funding', product_funding, name='product-funding'),
]
