import django_filters
class ProduuctFilter(django_filters.FilterSet):
    price=django_filters.NumberFilter(field_name='price',lookup_expr='lte')