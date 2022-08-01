from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer


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

    @action(methods=['post'], detail=False)
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            data = {'user': UserSerializer(user, context=self.get_serializer_context()).data,
                    'access': access,
                    'refresh': refresh}

            return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = {'user': serializer.validated_data['user'].email,
                    'access': serializer.validated_data['access'],
                    'refresh': serializer.validated_data['refresh']}

        return Response(data, status=status.HTTP_200_OK)
