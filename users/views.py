from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

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

        # 입력된 데이터가 지정된 형식과 다를 경우 예외처리
        if not serializer.is_valid(raise_exception=True):
            return Response({'error_message': '입력된 데이터의 형식을 확인하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=serializer.validated_data['email']).first() is None:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error_message': '이미 가입된 이메일입니다.'}, status=status.HTTP_409_CONFLICT)

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
