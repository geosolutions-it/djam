from typing import List
from django.conf import settings
from apps.billing.enums import SubscriptionTypeEnum
from apps.privilege_manager.models import Group
from apps.billing.models import Subscription
from django.utils import timezone


class SubscriptionException(Exception):
    pass


class SubscriptionManager:
    def create_individual_subscription(self, groups: Group, *args, **kwargs) -> Subscription:
        sub_type = SubscriptionTypeEnum.INDIVIDUAL
        # validation of the subscription
        return self._create_subscription(sub_type=sub_type, groups=groups, **kwargs)

    def create_company_subscription(self, groups: Group, *args, **kwargs) -> Subscription:
        sub_type = SubscriptionTypeEnum.COMPANY
        # validation of the subscription
        return self._create_subscription(sub_type=sub_type, groups=groups, **kwargs)

    def validate_subscription(self, sub_type, groups) -> None:
        assigned_groups = self._get_groups_name(groups)
        if sub_type == "INDIVIDUAL":
            return self._validate_individual_sub(assigned_groups)
        elif sub_type == "COMPANY":
            return self._validate_company_sub(assigned_groups)
        return False

    def get_active_user_subscription(self, user) -> List[Subscription]:
        return NotImplemented

    def _create_subscription(self, sub_type, groups: Group, **kwargs) -> Subscription:
        self.validate_subscription(sub_type, groups)

        # Creation of the base object
        sub = Subscription.objects.create()

        sub, _ = Subscription.objects.update_or_create(
            subscription_type=getattr(SubscriptionTypeEnum, sub_type),
            **kwargs
        )
        # Assign groups for the subscription
        sub.groups.add(groups)
        return sub

    def _get_groups_name(self, groups) -> List[str]:
        if isinstance(groups, Group):
            return [groups.name]
        else:
            return [g.name for g in groups.all()]

    @staticmethod
    def _validate_individual_sub(groups) -> bool:
        check = all(
            item.upper() in settings.ACCEPTED_PERMISSIONS_FOR_INDIVIDUALS_SUB
            for item in groups
        )
        if not check:
            raise SubscriptionException(
                "One of the selected groups is not valid for Individual subscription."
            )
        return check

    @staticmethod
    def _validate_company_sub(groups) -> bool:
        check = all(
            item.upper() in settings.ACCEPTED_PERMISSIONS_FOR_COMPANY_SUB for item in groups
        )
        if not check:
            raise SubscriptionException(
                "One of the selected groups is not valid for Company subscription."
            )
        return check
