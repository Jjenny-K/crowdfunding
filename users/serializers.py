from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.timezone import now

from users.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    """ 회원가입 serializer """
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )

        return user

    def validate(self, data):
        email = data.get('email', None)

        if User.objects.filter(email=email).exists():
            # 입력된 데이터에 해당하는 사용자가 있을 경우 예외처리
            raise serializers.ValidationError(
                '이미 가입된 이메일입니다.'
            )

        return data


class UserLoginSerializer(serializers.Serializer):
    """ 로그인 serializer """
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            # 입력된 데이터에 해당하는 사용자가 없을 경우 예외처리
            raise serializers.ValidationError(
                '이메일이나 비밀번호를 확인하세요.'
            )
        else:
            user.last_login = now()
            user.save(update_fields=['last_login'])

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            data = {'user': user,
                    'access': access,
                    'refresh': refresh}

            return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )
        read_only_fields = (
            'email',
        )
