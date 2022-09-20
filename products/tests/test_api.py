import pytest

from django.urls import reverse

from products.models import Product, Funding

pytestmark = pytest.mark.django_db


class Test_ProductAPI:
    @pytest.fixture
    def product_data(self, client, set_test_user):
        data = {
            'user': set_test_user,
            'name': 'test',
            'description': 'test product',
            'target_fund': 1000000,
            'fund_per_once': 10000,
            'end_date': '2022-09-30'
        }

        return data

    @pytest.fixture
    def set_test_product(self, client, set_test_user):
        product_obj = Product.objects.create(
            id=1,
            user=set_test_user,
            name='testtest',
            description='testtest product',
            target_fund=100000,
            fund_per_once=5000,
            end_date='2022-09-30'
        )

        return product_obj

    @pytest.fixture
    def funding_data(self, client, set_test_user, set_test_product):
        data = {
            'user': set_test_user,
            'product': set_test_product
        }

        return data

    @pytest.fixture
    def set_test_funding(self, client, set_test_user, set_test_product):
        funding_obj = Funding.objects.create(
            id=1,
            user=set_test_user,
            product=set_test_product
        )

        return funding_obj

    list_url = reverse('product-list')
    detail_url = 'product-detail'
    funding_url = 'product-funding'

    def test_create_product(self, client, product_data, get_user_headers):
        # POST api/products
        response = client.post(path=self.list_url, data=product_data, **get_user_headers)

        assert response.status_code == 201

    def test_list_products(self, client):
        # GET api/products
        response = client.get(path=self.list_url)

        assert response.status_code == 200

    def test_retrieve_product(self, client, set_test_product):
        # GET api/products/:pk
        url = reverse(self.detail_url, kwargs={'pk': '1'})
        response = client.get(path=url)

        assert response.status_code == 200

    def test_update_product_no_auth(self, client, set_test_product):
        # PUT api/products/:pk
        # 인증된 사용자 본인이 작성한 상품이 아닐 때 권한 제한
        url = reverse(self.detail_url, kwargs={'pk': '1'})
        response = client.put(path=url, data={'name': 'change', 'end_date': '2022-10-01'})

        assert response.status_code == 401

    def test_update_product_auth(self, client, set_test_product, get_user_headers):
        # PUT api/products/:pk
        url = reverse(self.detail_url, kwargs={'pk': '1'})
        response = client.put(path=url, data={'name': 'change', 'end_date': '2022-10-01'}, **get_user_headers)

        assert response.status_code == 200

    def test_destroy_product_no_auth(self, client, set_test_product):
        # DELETE api/products/:pk
        # 인증된 사용자 본인이 작성한 상품이 아닐 때 권한 제한
        url = reverse(self.detail_url, kwargs={'pk': '1'})
        response = client.delete(path=url)

        assert response.status_code == 401

    def test_destroy_product_auth(self, client, set_test_product, get_user_headers):
        # DELETE api/products/:pk
        url = reverse(self.detail_url, kwargs={'pk': '1'})
        response = client.delete(path=url, **get_user_headers)

        assert response.status_code == 204

    def test_create_funding(self, client, funding_data, get_user_headers):
        # POST api/products/:pk/funding
        url = reverse(self.funding_url, kwargs={'pk': '1'})
        response = client.post(path=url, **get_user_headers)

        assert response.status_code == 201

    def test_list_funding_no_auth(self, client, set_test_funding):
        # GET api/products/:pk/funding
        # 인증된 사용자 본인의 정보가 아닐 때 권한 제한
        url = reverse(self.funding_url, kwargs={'pk': '1'})
        response = client.get(path=url)

        assert response.status_code == 401

    def test_list_funding_auth(self, client, set_test_funding, get_user_headers):
        # GET api/products/:pk/funding
        # 인증된 사용자 본인의 정보가 아닐 때 권한 제한
        url = reverse(self.funding_url, kwargs={'pk': '1'})
        response = client.get(path=url, **get_user_headers)

        assert response.status_code == 200
