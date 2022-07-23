from rest_framework import serializers
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


class UserLoginSerializer(serializers.Serializer):
    """ 로그인 serializer """
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        # 입력된 데이터에 해당하는 사용자가 없을 경우 예외처리
        if user is None:
            raise serializers.ValidationError(
                '이메일이나 비밀번호를 확인하세요.'
            )
        else:
            user.last_login = now()
            user.save(update_fields=['last_login'])

            return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {
            'email',
            'username',
        }
        read_only_fields = (
            'email',
        )
