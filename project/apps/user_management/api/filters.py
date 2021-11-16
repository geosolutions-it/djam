import django_filters
from django.contrib.auth import get_user_model

from apps.billing.models import Subscription


class UsersFilterSet(django_filters.FilterSet):
    older = django_filters.IsoDateTimeFilter(lookup_expr='lt', field_name='last_login')
    newer = django_filters.IsoDateTimeFilter(lookup_expr='gt', field_name='last_login')
    older_equal = django_filters.IsoDateTimeFilter(lookup_expr='lte', field_name='last_login')
    newer_equal = django_filters.IsoDateTimeFilter(lookup_expr='gte', field_name='last_login')
    groups = django_filters.BaseInFilter(method='get_by_group')
    email_confirmation = django_filters.BooleanFilter(field_name='email_confirmed')

    class Meta:
        model = get_user_model()
        fields = ['older', 'older_equal', 'newer', 'newer_equal', 'groups', 'email_confirmation']

    def get_by_group(self, queryset, field_name, value):
        if value:
            sub = Subscription.objects.filter(groups__name__in=value).first()
            c_users = []
            i_users = []
            if sub:
                if hasattr(sub, "companysubscription"):
                    c_users = list(sub.companysubscription.company.users.values_list("id", flat=True))
                else:
                    i_users = [sub.individualsubscription.user.id] if sub.individualsubscription.is_active else []
            
            return queryset.filter(id__in=c_users+i_users).distinct()
        return queryset
