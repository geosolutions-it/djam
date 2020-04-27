import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import resolve_url
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, DetailView
from apps.user_management.forms import UserAccountForm

logger = logging.getLogger(__name__)


class UserGtObjectMixin:
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        id = self.kwargs.get(self.pk_url_kwarg)
        if id is None:
            id = self.request.user.id
        if int(id) != self.request.user.id:
            raise PermissionDenied(_("You are not allowed to see this page"))
        try:
            return queryset.get(**{self.pk_url_kwarg: id})
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )


class UMLoginView(LoginView):
    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(
            f"{settings.LOGIN_REDIRECT_URL}{self.request.user.id}/"
        )


class AccountPageView(UserGtObjectMixin, LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "account/user.html"
    pk_url_kwarg = "id"


class AccountEditView(UserGtObjectMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserAccountForm
    template_name = "account/user_edit.html"
    pk_url_kwarg = "id"

    def get_success_url(self):
        return f"/user/account/{self.object.id}"


class PasswordAccountEditView(UserGtObjectMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserAccountForm
    template_name = "account/password_change_done.html"
    pk_url_kwarg = "id"

    def get_success_url(self):
        return f"/user/account/{self.object.id}"
