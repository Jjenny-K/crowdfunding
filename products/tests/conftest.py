from pytest_factoryboy import register

from products.tests.factories import ProductFactory, FundingFactory

register(ProductFactory)
register(FundingFactory)
