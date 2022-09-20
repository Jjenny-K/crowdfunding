import pytest

from products.models import Product, Funding
from products.tests.factories import ProductFactory, FundingFactory

pytestmark = pytest.mark.django_db


def test_product_factory(product_factory):
    # faker로 생성한 product_factory가 ProductFactory의 형태인지 확인
    assert product_factory is ProductFactory


def test_product(product):
    # faker로 생성한 product가 Product model의 형태인지 확인
    assert isinstance(product, Product)


@pytest.mark.parametrize('product__fund_per_once', [5000])
def test_product_fund_per_once(product):
    # faker로 생성할 product에 파라미터 인자를 직접 전달해 생성 및 확인
    assert product.fund_per_once == 5000
    assert isinstance(product, Product)


def test_funding_factory(funding_factory):
    # faker로 생성한 funding_factory가 FundingFactory의 형태인지 확인
    assert funding_factory is FundingFactory


def test_funding(funding):
    # faker로 생성한 fundingd이 Funding model의 형태인지 확인
    assert isinstance(funding, Funding)


@pytest.mark.parametrize('product__target_fund', [500000])
def test_funding_product_target_fund(funding):
    # faker로 생성할 funding에 파라미터 인자를 직접 전달해 생성 및 확인
    assert funding.product.target_fund == 500000
    assert isinstance(funding, Funding)
