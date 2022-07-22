from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewset

user_router = DefaultRouter(trailing_slash=False)
user_router.register('users', UserViewset)

urlpatterns = [
    path('', include(user_router.urls)),
]
