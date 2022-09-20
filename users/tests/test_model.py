import pytest

from users.models import User
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_factory(user_factory):
    # faker로 생성한 user_factory가 UserFactory의 형태인지 확인
    assert user_factory is UserFactory


def test_user(user):
    # faker로 생성한 user가 User model의 형태인지 확인
    assert isinstance(user, User)


@pytest.mark.parametrize('user__password', ['test001!!'])
def test_user_passoword(user):
    # faker로 생성할 user에 파라미터 인자를 직접 전달해 생성 및 확인
    assert isinstance(user, User)
    assert user.password == 'test001!!'
