from apps.administration.models import CompanySubscription
from django import template

register = template.Library()

@register.filter
def get_company_sub(value):
    company_sub = CompanySubscription.objects.filter(company__users=value.user)
    if company_sub.exists():
        return company_sub.get()

@register.filter
def get_subscription_type(value):
    pass
