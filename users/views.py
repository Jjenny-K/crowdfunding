from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer
from users.permissions import IsOwnerOrReadOnly


class UserViewset(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'signup':
            return UserSignupSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action in ('signup', 'login'):
            permission_class = (AllowAny,)
        else:
            permission_class = (IsOwnerOrReadOnly,)

        return [permission() for permission in permission_class]

    @action(methods=['post'], detail=False)
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({'message': f'{serializer.data["username"]}님 가입을 환영합니다.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = {'user': serializer.validated_data['user'].email,
                    'access': serializer.validated_data['access'],
                    'refresh': serializer.validated_data['refresh']}

        return Response(data, status=status.HTTP_200_OK)
