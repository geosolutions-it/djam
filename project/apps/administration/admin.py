from django.contrib.auth import get_user_model
from apps.administration.models import ClientManagementModel
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Register your models here.

@admin.register(ClientManagementModel)
class ClientManagementAdmin(admin.ModelAdmin):
    #change_list_template = 'admin/client/change_list.html'

    object_history_template = []

    list_display = [
        "email",
        "first_name",
        "last_name",
    ]

    search_fields = ['username']

    def get_queryset(self, request):
        qs = get_user_model().objects.all()
        return qs

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)

    def get_actions(self, request):
        return {}

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return request.user.is_superuser

    #def changelist_view(self, request, extra_context=None):
    #    extra_context = extra_context or {}
    #    extra_context['some_var'] = 'This is what I want to show'
    #    return super(ClientManagementAdmin, self).changelist_view(request, extra_context=extra_context)
#
    #def get_search_results(self, request, queryset, search_term):
    #    queryset, use_distinct = super().get_search_results(request, queryset, search_term)
    #    try:
    #        search_term_as_int = int(search_term)
    #    except ValueError:
    #        pass
    #    else:
    #        queryset |= self.model.objects.filter(age=search_term_as_int)
    #    return queryset, use_distinct
