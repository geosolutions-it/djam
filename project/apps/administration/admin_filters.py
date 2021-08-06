from django.contrib.admin import SimpleListFilter

class IsActiveCustomFilter(SimpleListFilter):
    title = 'is_active'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return [(True, True), (False, False)]

    def queryset(self, request, queryset):
        if request.GET.get('is_active', None):
            ids = [s.id for s in queryset if s.is_active is bool(request.GET.get('is_active', None))]
            queryset = queryset.filter(id__in=ids)
        return queryset

class SubscriptionTypeFilter(SimpleListFilter):
    title = 'subscription type'
    parameter_name = 'sub_type'

    def lookups(self, request, model_admin):
        return [('INDIVIDUAL', 'INDIVIDUAL'), ('COMPANY', 'COMPANY')]

    def queryset(self, request, queryset):
        if request.GET.get('sub_type', None):
            ids = [s.id for s in queryset if s.subscription_type == request.GET.get('sub_type', None)]
            queryset = queryset.filter(id__in=ids)
        return queryset
