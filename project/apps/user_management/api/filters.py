import django_filters
from django.contrib.auth import get_user_model


class UsersFilterSet(django_filters.FilterSet):
    older = django_filters.IsoDateTimeFilter(lookup_expr="lt", field_name="last_login")
    newer = django_filters.IsoDateTimeFilter(lookup_expr="gt", field_name="last_login")
    older_equal = django_filters.IsoDateTimeFilter(
        lookup_expr="lte", field_name="last_login"
    )
    newer_equal = django_filters.IsoDateTimeFilter(
        lookup_expr="gte", field_name="last_login"
    )
    groups = django_filters.BaseInFilter(method="get_by_group")
    email_confirmation = django_filters.BooleanFilter(field_name="email_confirmed")

    class Meta:
        model = get_user_model()
        fields = [
            "older",
            "older_equal",
            "newer",
            "newer_equal",
            "groups",
            "email_confirmation",
        ]

    def get_by_group(self, queryset, field_name, value):
        return queryset.distinct()
