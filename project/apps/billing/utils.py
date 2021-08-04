from operator import sub
from apps.user_management.models import User
from typing import List, Optional, Union
from django.conf import settings
from apps.billing.enums import SubscriptionTypeEnum
from apps.privilege_manager.models import Group
from apps.billing.models import Subscription
from django.db.models import QuerySet

class SubscriptionException(Exception):
    pass


class SubscriptionManager:
    def create_individual_subscription(self, groups: Group, users: User = None, *args, **kwargs) -> Subscription:
        """
        Create an individual subscription:
        - groups: Group object or Queryset of groups
        """
        sub_type = SubscriptionTypeEnum.INDIVIDUAL
        # validation of the subscription
        return self._create_subscription(sub_type=sub_type, groups=groups, users=users, **kwargs)

    def create_company_subscription(self, groups: Group, users: User = None, *args, **kwargs) -> Subscription:
        """
        Create a company subscription:
        - groups: Group object or Queryset of groups
        """        
        sub_type = SubscriptionTypeEnum.COMPANY
        # validation of the subscription
        return self._create_subscription(sub_type=sub_type, groups=groups, users=users, **kwargs)

    def validate_subscription(self, sub_type: str, groups: List[Group], users: List[User] = None) -> bool:
        """
        Return if the subscrption proposed is valid:
        - subscription type INDIVIDUAL or COMPANY
        - groups: list of group names
        """
        is_valid_groups = True
        is_valid_user = True
        if groups is not None:
            is_valid_groups = self.validate_groups(sub_type=sub_type, groups=groups)
        if users is not None:
            is_valid_user = self.can_add_new_subscription_by_user(users, sub_type=sub_type)
        return all((is_valid_user, is_valid_groups))

    def can_add_new_subscription_by_user(self, user: User, sub_type: Optional[str] = None) -> bool:
        """
        Return true if the selected user have new subscriptions
        """
        active_subs = self.get_active_subscription_by_user(user)
        ind = len(active_subs.get(SubscriptionTypeEnum.INDIVIDUAL))
        comp = len(active_subs.get(SubscriptionTypeEnum.COMPANY))
        if ind == 0 and comp == 0:
            return True
        elif sub_type is None:
            if ind + comp >= 2:
                return False
            return ind <= 1 and comp <= 1
        else:
            if not len(active_subs.get(sub_type)) < 1:
                raise SubscriptionException(
                    f"The selected users is not valid for this {sub_type} subscription."
                )
            return True

    def get_active_subscription_by_user(self, user: Union[User, QuerySet]) -> List[Subscription]:
        """
        Get all the subscription active for a specific user in a dictionary with 
        information about the subscription type
        - user: User object
        """           
        subs = {
            'INDIVIDUAL': [],
            'COMPANY': []
        }
        if not isinstance(user, QuerySet):
            user = [user]
        for usr in user:
            subs['INDIVIDUAL'].extend(self._get_active_subscription_by_user(user=usr, sub_type=SubscriptionTypeEnum.INDIVIDUAL))
            subs['COMPANY'].extend(self._get_active_subscription_by_user(user=usr, sub_type=SubscriptionTypeEnum.COMPANY))
        return subs

    def validate_groups(self, groups, sub_type):
        assigned_groups = self._get_groups_name(groups)
        if sub_type == "INDIVIDUAL":
            return self._validate_individual_sub(assigned_groups)
        elif sub_type == "COMPANY":
            return self._validate_company_sub(assigned_groups)
        return False

    def _get_active_subscription_by_user(self, user: User, sub_type: str) -> Optional[List]:
        """
        Get all the subscription active for a specific user
        - user: User object
        - sub_type: INDIVIDUAL or COMPANY
        """            
        subs = Subscription.objects.filter(users=user, subscription_type=sub_type)
        return [sub for sub in subs if sub.is_active()]

    def _create_subscription(self, sub_type, groups: Group, users: User, **kwargs) -> Subscription:
        """
        Create the subscription
        """
        self.validate_subscription(sub_type, groups, users)

        # Creation of the base object
        sub = Subscription.objects.create()

        sub, _ = Subscription.objects.update_or_create(
            subscription_type=getattr(SubscriptionTypeEnum, sub_type),
            **kwargs
        )
        # Assign groups for the subscription
        if groups is not None:
            sub.groups.add(groups)
        if users is not None:
            sub.users.add(users)
        return sub

    def _get_groups_name(self, groups: Union[Group, QuerySet]) -> List[str]:
        if isinstance(groups, Group):
            return [groups.name]
        else:
            return [g.name for g in groups.all()]

    @staticmethod
    def _validate_individual_sub(groups: List[str]) -> bool:
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
    def _validate_company_sub(groups: List[str]) -> bool:
        check = all(
            item.upper() in settings.ACCEPTED_PERMISSIONS_FOR_COMPANY_SUB for item in groups
        )
        if not check:
            raise SubscriptionException(
                "One of the selected groups is not valid for Company subscription."
            )
        return check
