from django.contrib import admin

from products.models import Product, Funding

admin.site.register([Product, Funding])
