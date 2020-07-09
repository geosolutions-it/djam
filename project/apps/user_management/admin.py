from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from apps.user_management.forms import UMAdminUserCreationForm, UMAdminUserChangeForm


@admin.register(get_user_model())
class IPUserAdmin(UserAdmin):
    add_form = UMAdminUserCreationForm
    form = UMAdminUserChangeForm
    model = get_user_model()
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
    ]

    fieldsets = (
        (None, {"fields": ("email", "password", "email_confirmed")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2",),}),
    )
