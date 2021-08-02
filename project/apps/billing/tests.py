from apps.billing.utils import SubscriptionException, SubscriptionManager
from apps.billing.models import Subscription
from apps.privilege_manager.models import Group
from django.test import TestCase
from datetime import timedelta
from django.utils import timezone

# Create your tests here.

class SubscriptionManagerTest(TestCase):
    def setUp(self):
        self.sut = SubscriptionManager()
        self.free_group = Group.objects.get(name='free')
        self.pro_group = Group.objects.get(name='pro')
        self.enterprise_group = Group.objects.get(name='enterprise')

    def test_indivitual_sub_free_group(self):
        """
        Given FREE group CAN create an INDIVIDUAL sub
        """
        subscription = self.sut.create_individual_subscription(
            groups=self.free_group
        )
        self.assertIsNotNone(subscription)

    def test_indivitual_sub_pro_group(self):
        """
        Given PRO group CAN create an INDIVIDUAL sub
        """
        subscription = self.sut.create_individual_subscription(groups=self.pro_group)
        self.assertIsNotNone(subscription)

    def test_indivitual_sub_enterprise_group(self):
        """
        Given ENTERPRISE group CANNOT create an INDIVIDUAL sub
        """
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_individual_subscription(groups=self.enterprise_group)

    def test_company_sub_enterprise_group(self):
        """
        Given ENTERPRISE group CAN create a COMPANY sub
        """
        subscription = self.sut.create_company_subscription(groups=self.enterprise_group)
        self.assertIsNotNone(subscription)

    def test_company_sub_free_group(self):
        """
        Given FREE group CANNOT create an COMPANY sub
        """
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_company_subscription(groups=self.free_group)

    def test_company_sub_pro_group(self):
        """
        Given PRO group CANNOT create an COMPANY sub
        """
        with self.assertRaises(SubscriptionException) as e:
            self.sut.create_company_subscription(groups=self.pro_group)


class SubscriptionModelTests(TestCase):
    def test_subscription_is_active(self):
        """
        Given a subscription, will check if the subscription is still active
        """
        sub, _ = Subscription.objects.get_or_create(
            start_timestamp=timezone.now(),
            end_timestamp=(timezone.now() + timedelta(days=3))
        )
        is_active = sub.is_active()
        self.assertTrue(is_active)

    def test_subscription_is_inactive(self):
        """
        Given a subscription, will check if the subscription is still active
        """
        sub, _ = Subscription.objects.get_or_create(
            start_timestamp=timezone.now(),
            end_timestamp=(timezone.now() - timedelta(days=3))
        )
        is_active = sub.is_active()
        self.assertFalse(is_active)

    def test_subscription_is_active_without_end_date(self):
        """
        Given a subscription without end_date, is considered valid
        """
        sub, _ = Subscription.objects.get_or_create(
            end_timestamp=None
        )
        is_active = sub.is_active()
        self.assertTrue(is_active)
