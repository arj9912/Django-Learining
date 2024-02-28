from django_filters.rest_framework import FilterSet
from store.models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        # fields = ["collecton_id","unit_price"]
        fields ={
            "collection_id": ["exact"],
            "unit_price": ["gt","lt"],

        }