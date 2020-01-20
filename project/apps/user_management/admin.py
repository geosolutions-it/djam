from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from apps.user_management.forms import UMAdminUserCreationForm, UMAdminUserChangeForm


@admin.register(get_user_model())
class IPUserAdmin(UserAdmin):
    add_form = UMAdminUserCreationForm
    form = UMAdminUserChangeForm
    model = get_user_model()
    list_display = ['email', 'username',]
