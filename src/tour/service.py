from django_filters import rest_framework as filters
from .models import Tour


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TourFilter(filters.FilterSet):
    category = CharFilterInFilter(field_name="category__slug", lookup_expr="in")
    region = CharFilterInFilter(field_name="region__slug", lookup_expr="in")
    guide = CharFilterInFilter(field_name="guide__slug", lookup_expr="in")
    complexity = CharFilterInFilter(field_name="complexity", lookup_expr="in")
    duration = CharFilterInFilter(field_name="duration", lookup_expr="in")
    price = filters.RangeFilter(field_name="price", lookup_expr="in")
    date_departure = filters.DateFilter()

    class Meta:
        model = Tour
        fields = "category region guide date_departure date_arrival complexity duration price".split()
