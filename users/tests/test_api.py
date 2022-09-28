import pytest

from django.urls import reverse

pytestmark = pytest.mark.django_db


class Test_UserAPI:
    user_data = {
        'email': 'test@email.com',
        'username': 'test',
        'password': 'test1234!'
    }

    login_user_data = {
        'email': 'testuser@email.com',
        'password': 'testuser1234!'
    }

    list_url = reverse('users-list')
    detail_url = 'users-detail'

    def test_signup(self, client):
        url = 'http://127.0.0.1/api/users/signup'
        response = client.post(path=url, data=self.user_data)

        assert response.status_code == 201

    def test_login(self, client, set_test_user):
        url = 'http://127.0.0.1/api/users/login'
        response = client.post(path=url, data=self.login_user_data)

        assert response.status_code == 200

    def test_list_users_no_auth(self, client):
        # GET api/users
        # 인증된 사용자가 아닐 때 권한 제한
        response = client.get(path=self.list_url)

        assert response.status_code == 401

    def test_list_users_auth(self, client, get_user_headers):
        # GET api/users
        response = client.get(path=self.list_url, **get_user_headers)

        assert response.status_code == 200

    def test_retrieve_user_no_auth(self, client):
        # GET api/users/:pk
        # 인증된 사용자 본인의 정보가 아닐 때 권한 제한
        url = reverse(self.detail_url, kwargs={'pk': '1'})
        response = client.get(path=url)

        assert response.status_code == 401

    def test_retrieve_user_auth(self, client, get_user_headers):
        # GET api/users/:pk
        url = reverse(self.detail_url, kwargs={'pk': '2'})
        response = client.get(path=url, **get_user_headers)

        assert response.status_code == 200

    def test_update_user_no_auth(self, client, get_user_headers):
        # PUT api/users/:pk
        # 인증된 사용자 본인의 정보가 아닐 때 권한 제한
        url = reverse(self.detail_url, kwargs={'pk': '1'})
        response = client.put(path=url, data={'username': 'testtest'}, **get_user_headers)

        assert response.status_code == 403

    def test_update_user_auth(self, client, get_user_headers):
        # PUT api/users/:pk
        url = reverse(self.detail_url, kwargs={'pk': '2'})
        response = client.put(path=url, data={'username': 'testtest'}, **get_user_headers)

        assert response.status_code == 200

    def test_destroy_user_no_auth(self, client, get_user_headers):
        # DELETE api/users/:pk
        # 인증된 사용자 본인의 정보가 아닐 때 권한 제한
        url = reverse(self.detail_url, kwargs={'pk': '1'})
        response_01 = client.delete(path=url, **get_user_headers)
        response_02 = client.get(path=url, **get_user_headers)

        assert response_01.status_code == 403
        assert response_02.status_code == 403

    def test_destroy_user_auth(self, client, get_user_headers):
        # DELETE api/users/:pk
        url = reverse(self.detail_url, kwargs={'pk': '2'})
        response_01 = client.delete(path=url, **get_user_headers)
        response_02 = client.get(path=url, **get_user_headers)

        assert response_01.status_code == 204
        assert response_02.status_code == 401
