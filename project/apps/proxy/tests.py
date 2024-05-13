from datetime import datetime
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.identity_provider.models import ApiKey
from tests.factories.user_management_factory import (
    ResourceFactory,
    RoleFactory,
    TeamFactory,
    UserFactory,
)
from apps.authorizations.models import AccessRule
import base64
from rest_framework import HTTP_HEADER_ENCODING

# Create your tests here.


class TestProxyView(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user_1 = UserFactory()
        cls.user_2 = UserFactory()
        cls.user_with_team = UserFactory()
        cls.team = TeamFactory()
        cls.role_1 = RoleFactory()
        cls.resource1 = ResourceFactory()
        cls.resource2 = ResourceFactory(type="invalid_type", path="path_to_find")
        # assign the path to the resource
        cls.resource1.path = "path_to_find"
        cls.resource1.url = "http://proxyto.com"
        cls.resource1.save()
        cls.proxy_url = reverse("proxy_view", args=["path_to_find"])
        return super().setUpClass()

    def test_anonymous_cannot_access(self):
        """
        anonymous doesn't have any permission to access the proxied service
        """
        try:
            # no access rules defined
            self.assertFalse(AccessRule.objects.all().exists())

            response = self.client.get(self.proxy_url)
            self.assertEqual(403, response.status_code)

        finally:
            AccessRule.objects.all().delete()

    def test_authenticated_ser_with_no_rules_available(self):
        """
        User 1 does not have any permission to access resource 1 via access_rule1
        """
        try:
            # no access rules defined
            self.assertFalse(AccessRule.objects.all().exists())

            self.client.force_login(self.user_1)

            response = self.client.get(self.proxy_url)
            self.assertEqual(403, response.status_code)

        finally:
            AccessRule.objects.all().delete()

    def test_should_raise_error_if_url_is_not_defined_in_the_resource(self):
        """
        Should raise an exception if the URL is not defined for a resource
        """
        try:
            # no access rules defined
            self.assertFalse(AccessRule.objects.all().exists())

            self.client.force_login(self.user_1)

            # assign the role to the user
            self.user_1.role.set([self.role_1])
            self.user_1.save()
            # removing the url from the resource
            self.resource1.url = ""
            self.resource1.save()

            # create the rule
            AccessRule.objects.create(
                resource=self.resource1, role=self.role_1, active=True
            )
            with self.assertRaises(Exception):
                response = self.client.get(self.proxy_url)

        finally:
            AccessRule.objects.all().delete()

    def test_should_return_empty_response_for_not_upstream_service_type(self):
        """
        For now we accept only UPSTREAM_SERVICE as service type.
        If is not that type the proxy should redirect to an empty response
        """
        try:
            # no access rules defined
            self.assertFalse(AccessRule.objects.all().exists())

            self.client.force_login(self.user_1)

            # assign the role to the user
            self.user_1.role.set([self.role_1])
            self.user_1.save()

            # create the rule
            AccessRule.objects.create(
                resource=self.resource2, role=self.role_1, active=True
            )

            response = self.client.get(self.proxy_url)
            self.assertEqual(204, response.status_code)

        finally:
            AccessRule.objects.all().delete()

    def test_user_with_perms_canot_be_proxed_if_rule_is_not_active(self):
        """
        User 1 matches the accesrule, but active is false
        which means that the rule is not active and the is denied
        """
        try:
            # no access rules defined
            self.assertFalse(AccessRule.objects.all().exists())

            self.client.force_login(self.user_1)

            # assign the role to the user
            self.user_1.role.set([self.role_1])
            self.user_1.save()

            # create the rule
            AccessRule.objects.create(
                resource=self.resource1, role=self.role_1, active=False
            )

            response = self.client.get(self.proxy_url)
            self.assertEqual(403, response.status_code)

        finally:
            AccessRule.objects.all().delete()

    def test_user_with_perms_can_be_proxed(self):
        """
        User 1 can access resource 1 via access_rule1
        """
        try:
            # no access rules defined
            self.assertFalse(AccessRule.objects.all().exists())

            self.client.force_login(self.user_1)

            # assign the role to the user
            self.user_1.role.set([self.role_1])
            self.user_1.save()

            # create the rule
            AccessRule.objects.create(
                resource=self.resource1, role=self.role_1, active=True
            )

            response = self.client.get(self.proxy_url)
            self.assertEqual(302, response.status_code)

        finally:
            AccessRule.objects.all().delete()

    def test_team_with_perms_can_be_proxed(self):
        """
        User of team 1 can access resource 1 since team 1 has a rule for its role
        """
        try:
            # no access rules defined
            self.assertFalse(AccessRule.objects.all().exists())

            self.client.force_login(self.user_1)
            # assign the team to the user
            self.user_1.team.set([self.team])
            # assign the role to the team
            self.team.role.set([self.role_1])
            self.team.save()

            # create the rule
            AccessRule.objects.create(
                resource=self.resource1, role=self.role_1, active=True
            )

            response = self.client.get(self.proxy_url)
            self.assertEqual(302, response.status_code)

            # user without that team cannot access
            self.client.force_login(self.user_2)

            response = self.client.get(self.proxy_url)
            self.assertEqual(403, response.status_code)

        finally:
            AccessRule.objects.all().delete()

    def test_team_with_perms_can_be_proxed_by_accessing_via_basic_auth(self):
        """
        Access with basic auth should work and the user should be proxed
        """
        try:
            # no access rules defined
            self.assertFalse(AccessRule.objects.all().exists())
            # assign the team to the user
            self.setupteam()

            # create the rule
            AccessRule.objects.create(
                resource=self.resource1, role=self.role_1, active=True
            )
            credentials = f"{self.user_1.username}:abc123"
            base64_credentials = base64.b64encode(
                credentials.encode(HTTP_HEADER_ENCODING)
            ).decode(HTTP_HEADER_ENCODING)

            response = self.client.get(
                self.proxy_url, HTTP_AUTHORIZATION=f"Basic {base64_credentials}"
            )
            self.assertEqual(302, response.status_code)

            # user without that team cannot access
            self.client.force_login(self.user_2)

            response = self.client.get(self.proxy_url)
            self.assertEqual(403, response.status_code)

        finally:
            AccessRule.objects.all().delete()

    def test_team_with_perms_can_be_proxed_by_accessing_via_authtoken(self):
        """
        Access with basic auth should work and the user should be proxed
        """
        try:
            # no access rules defined
            self.assertFalse(AccessRule.objects.all().exists())
            # assign the team to the user
            self.setupteam()

            # create the rule
            AccessRule.objects.create(
                resource=self.resource1, role=self.role_1, active=True
            )

            # create djam api token
            token, created = ApiKey.objects.get_or_create(
                user=self.user_1, last_modified=datetime.utcnow()
            )
            url = f"{self.proxy_url}?authkey={str(token.key)}"
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

            # user without that team cannot access
            self.client.force_login(self.user_2)

            url = f"{self.proxy_url}?authkey=abc12345"
            response = self.client.get(self.proxy_url)
            self.assertEqual(403, response.status_code)

        finally:
            AccessRule.objects.all().delete()

    def setupteam(self):
        self.user_1.team.set([self.team])
        self.user_1.set_password("abc123")
        self.user_1.is_active = True
        self.user_1.save()
        # assign the role to the team
        self.team.role.set([self.role_1])
        self.team.save()
