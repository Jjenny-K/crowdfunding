from django.db import models


class TimestampZone(models.Model):
    created_at = models.DateTimeField(verbose_name='등록 날짜', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정 날짜', auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']
