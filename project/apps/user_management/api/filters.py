import itertools
import django_filters
from django.contrib.auth import get_user_model

from apps.billing.models import Subscription


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
        if value:
            subs = Subscription.objects.filter(groups__name__in=value)
            c_users = []
            i_users = []
            for sub in subs:
                if hasattr(sub, "companysubscription"):
                    c_users.extend(
                        list(
                            sub.companysubscription.company.users.values_list(
                                "id", flat=True
                            )
                        )
                    )
                else:
                    if not sub.individualsubscription.is_active:
                        continue
                    i_users.append(sub.individualsubscription.user.id)

            return queryset.filter(id__in=c_users + i_users).distinct()
        return queryset
