from django.urls import path

from products.views import ProductListViews, ProductDetailView

urlpatterns = [
    path('products', ProductListViews.as_view()),
    path('products/<int:pk>', ProductDetailView.as_view()),
]
