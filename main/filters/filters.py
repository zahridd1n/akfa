import django_filters
from ..models import Product, Order


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="exact")
    material = django_filters.CharFilter(field_name="material", lookup_expr="exact")
    design_style = django_filters.CharFilter(field_name="design_style", lookup_expr="exact")
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    badge = django_filters.CharFilter(field_name="badge", lookup_expr="exact")
    min_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="lte")
    is_active = django_filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = Product
        fields = ["category", "material", "design_style", "status", "badge", "is_active"]


class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    date_from = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Order
        fields = ["status"]
