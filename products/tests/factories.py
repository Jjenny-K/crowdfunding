import factory
from faker import Faker

from products.models import Product, Funding
from users.tests.factories import UserFactory

fake = Faker('ko_KR')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    user = factory.SubFactory(UserFactory)
    name = fake.word()
    description = fake.catch_phrase()
    target_fund = fake.random_int(100000, 1000000)
    fund_per_once = fake.random_int(1000, 100000)
    end_date = fake.date_time()


class FundingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Funding

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
