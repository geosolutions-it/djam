from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.identity_provider.models import ApiKey
from apps.privilege_manager.models import Group, OpenIdLoginPrevention
from django.contrib.auth.models import Group as DefaultGroup

# un-registration of Django auth Group model in admin page
admin.site.unregister(DefaultGroup)
admin.site.register(OpenIdLoginPrevention)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)

    def save_model(self, request, obj, form, change):
        if Group.GroupNames.ENTERPRISE.value == obj.name:
            self._generate_api_key_for_enterprise_user(form)

        super(GroupAdmin, self).save_model(request, obj, form, change)

    def _generate_api_key_for_enterprise_user(self, form):
        if 'users' in form.changed_data:
            initial_users = set(form.initial.get('users'))
            new_users = set(form.cleaned_data.get('users'))
            users_to_create = new_users - initial_users

            if users_to_create != set():
                # for this users create api keys
                for user in users_to_create:
                    ApiKey.objects.create(user=user)

            users_to_revoke = initial_users - new_users
            if users_to_revoke != set():
                # for this users revoke api keys
                ApiKey.objects.filter(user__in=users_to_revoke).update(revoked=True)
