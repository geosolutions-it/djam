import logging
from apps.billing.models import Subscription
from apps.administration.models import CompanySubscription, IndividualSubscription
from apps.identity_provider.models import ApiKey
from apps.hubspot_integration.utils import get_hubspot_subscription

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, resolve_url
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, DetailView, RedirectView
from apps.user_management.forms import UserAccountForm
from apps.privilege_manager.models import Group
from django.db.models import Q

logger = logging.getLogger(__name__)


class ProfileRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse('user_account', kwargs={
                'id': self.request.user.pk
            })
        return reverse(settings.HOME_VIEW)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fix_error'] = self.request.GET.get('fix_error')
        context['group'] = Group.objects.filter(users=context['object']).first()
        context['api_key'] = ApiKey.objects.filter(user=context['object']).first()
        context['success'] = self.request.GET.get('success')
        context['mail_subscription'] = get_hubspot_subscription(context['object'])
        context['individual_subscriptions'] = IndividualSubscription.objects.filter(user=context['object']).first()
        context['company_subscriptions'] = CompanySubscription.objects.filter(company__users=context['object'])
        return context

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'request': self.request,
        }
        self.object = form.save(**opts)
        context = self.get_context_data()
        context['success'] = True
        return render(self.request, self.template_name, context)
