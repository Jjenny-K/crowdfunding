from django.utils.timezone import now
from django.db import models

from utils.timestamp import TimestampZone


class Product(TimestampZone):
    user = models.ForeignKey('users.User', verbose_name='게시자', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='상품 이름', max_length=127)
    description = models.TextField(verbose_name='상품 설명', blank=True, default='')
    target_fund = models.PositiveIntegerField(verbose_name='목표 금액')
    fund_per_once = models.PositiveIntegerField(verbose_name='1회 펀딩 금액', default=0)
    total_fund = models.PositiveIntegerField(verbose_name='총 펀딩 금액', default=0)
    end_date = models.DateTimeField(verbose_name='펀딩 종료일')

    @property
    def achievement_rate(self):
        """ 달성률 """
        return f'{self.total_fund / self.target_fund * 100 if self.target_fund != 0 else 0: .0f}%'

    @property
    def d_day(self):
        """ D-day """
        return (self.end_date.date() - now().date()).days

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name


class Funding(TimestampZone):
    user = models.ForeignKey('users.User', verbose_name='펀딩자', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', verbose_name='펀딩 상품', on_delete=models.CASCADE)

    class Meta:
        db_table = 'funding'

    def __str__(self):
        return f'funding product({self.user}-{self.product})'
