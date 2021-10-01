
from datetime import timedelta
from django.utils import timezone
from apps.billing.models import Subscription
from django.test import TestCase


class SubscriptionModelTests(TestCase):
    def test_subscription_is_active(self):
        """
        Given a subscription, will check if the subscription is still active
        """
        sub, _ = Subscription.objects.get_or_create(
            start_timestamp=timezone.now(),
            end_timestamp=(timezone.now() + timedelta(days=3))
        )
        is_active = sub.is_active(
        self.assertTrue(is_active)

    def test_subscription_is_inactive(self):
        """
        Given a subscription, will check if the subscription is still active
        """
        sub, _ = Subscription.objects.get_or_create(
            start_timestamp=timezone.now(),
            end_timestamp=(timezone.now() - timedelta(days=3))
        )
        is_active = sub.is_active
        self.assertFalse(is_active)

    def test_subscription_is_active_without_end_date(self):
        """
        Given a subscription without end_date, is considered valid
        """
        sub, _ = Subscription.objects.get_or_create(
            end_timestamp=None
        )
        is_active = sub.is_active
        self.assertTrue(is_active)
