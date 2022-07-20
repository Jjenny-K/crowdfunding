from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.timestamp import TimestampZone


class User(AbstractUser, TimestampZone):
    class Meta:
        db_table = "user"
