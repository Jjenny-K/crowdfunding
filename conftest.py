import pytest

from django.core.management import call_command
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'testdata.json')


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def set_test_user(client):
    user_obj = User.objects.create_user(
        id=2,
        email='testuser@email.com',
        username='testuser',
        password='testuser1234!'
    )

    return user_obj


@pytest.fixture()
def get_user_headers(client, set_test_user):
    url = 'http://127.0.0.1/api/users/login'
    user_data = {'email': 'testuser@email.com', 'password': 'testuser1234!'}
    response = client.post(path=url, data=user_data)
    headers = response.data['access']
    headers = {'HTTP_AUTHORIZATION': f'Bearer {headers}'}
    return headers


def pytest_assertrepr_compare(left, right, op):
    print("Assertion 왼쪽 값은 {0}, 오른쪽 값은 {1}, 비교 값은 {2}".format(left, right, op))
