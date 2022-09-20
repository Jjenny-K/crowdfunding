import factory
from faker import Faker

from users.models import User

fake = Faker('ko_KR')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = fake.free_email()
    username = fake.user_name()
    password = fake.word()
