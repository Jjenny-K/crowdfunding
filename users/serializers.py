from rest_framework import serializers
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


class UserLoginSerializer(serializers.ModelSerializer):
    """ 로그인 serializer """
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        email = data.get('email', None)
        user = User.objects.filter(email=email).first()

        if user is None:
            return None
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
