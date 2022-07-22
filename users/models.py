from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from utils.timestamp import TimestampZone


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **kwargs):
        """ user 생성 """
        if not email:
            raise ValueError('must have user email')
        if not username:
            raise ValueError('must have user name')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None, **kwargs):
        """ superuser 생성 """
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            **kwargs
        )
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, TimestampZone):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=15)

    # Django User model 필수 fields
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # user 생성 헬퍼 클래스 지정
    objects = UserManager()

    # Django login 시스템 상 username 및 필수 작성 fields 설정
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username
