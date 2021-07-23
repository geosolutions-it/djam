from django.test.utils import override_settings
from apps.hubspot_integration.utils import get_hubspot_subscription
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import MagicMock, patch

class TestHubspotIntegration(TestCase):
    def setUp(self):
        self.user, _ = get_user_model().objects.get_or_create(username='admin')
        self.user.email = "fakemail@gmail.com"
        self.user.save()

    @override_settings(HUBSPOT_API_KEY="api-key")
    @patch('apps.hubspot_integration.utils.requests.get')
    def test_get_hubspot_subscription_for_subscribed_user_with_subscribed_false(self, get_mock):
        get_mock.return_value = MagicMock(status_code = 200)
        get_mock.return_value.json.return_value = {
            "subscribed": True,
            "markedAsSpam": False,
            "unsubscribeFromPortal": False,
            "portalId": 123,
            "bounced": False,
            "email": "fakemail@gmail.com",
            "subscriptionStatuses": [
                {
                "id": 123,
                "updatedAt": 123,
                "subscribed": True,
                "optState": "OPT_IN",
                "legalBasis": "LEGITIMATE_INTEREST_CLIENT",
                "legalBasisExplanation": "legal notes"
                },
                {
                "id": 5579305,
                "updatedAt": 123,
                "subscribed": False,
                "optState": "OPT_OUT"
                }
            ],
            "status": "subscribed"
            }
        self.assertFalse(get_hubspot_subscription(self.user))

    @override_settings(HUBSPOT_API_KEY="api-key")
    @patch('apps.hubspot_integration.utils.requests.get')
    def test_get_hubspot_subscription_for_subscribed_user_with_subscribed_true(self, get_mock):
        get_mock.return_value = MagicMock(status_code = 200)
        get_mock.return_value.json.return_value = {
            "subscribed": True,
            "markedAsSpam": False,
            "unsubscribeFromPortal": False,
            "portalId": 123,
            "bounced": False,
            "email": "fakemail@gmail.com",
            "subscriptionStatuses": [
                {
                "id": 123,
                "updatedAt": 123,
                "subscribed": True,
                "optState": "OPT_IN",
                "legalBasis": "LEGITIMATE_INTEREST_CLIENT",
                "legalBasisExplanation": "legal notes"
                },
                {
                "id": 5579305,
                "updatedAt": 123,
                "subscribed": True,
                "optState": "OPT_OUT"
                }
            ],
            "status": "subscribed"
            }
        self.assertTrue(get_hubspot_subscription(self.user))

    @override_settings(HUBSPOT_API_KEY="api-key")
    @patch('apps.hubspot_integration.utils.requests.get')
    def test_get_hubspot_subscription_for_non_subscribed_user(self, get_mock):
        get_mock.return_value = MagicMock(status_code = 200)
        get_mock.return_value.json.return_value = {
            "subscribed": True,
            "markedAsSpam": False,
            "unsubscribeFromPortal": False,
            "portalId": 123,
            "bounced": False,
            "email": "fakemail@gmail.com",
            "subscriptionStatuses": [
            ],
            "status": "subscribed"
            }
        self.assertFalse(get_hubspot_subscription(self.user))

