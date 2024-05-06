from django.test import TestCase, Client

from apps.privilege_manager.utils import has_login_permission

from tests.factories.user_management_factory import UserFactory, GroupFactory
from tests.factories.identity_provider_factory import (
    OIDCConfidentialClientFactory,
    OpenIdLoginPreventionFactory,
)


class PrivilegeManagerBaseTestCase(TestCase):
    def privilege_geoserver_roles(self, web_client: Client):
        return web_client.get("/api/privilege/geoserver/roles",)

    def privilege_geoserver_users(self, web_client: Client):
        return web_client.get("/api/privilege/geoserver/users",)


class TestPrivilegeManager(PrivilegeManagerBaseTestCase,):
    def test_geosever_roles_response(self):
        user = UserFactory()
        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        privilege_response = self.privilege_geoserver_roles(web_client)
        privilege_response.json()["groups"].sort()
        self.assertDictEqual(
            privilege_response.json(),
            {"groups": ["admin", "enterprise", "free", "pro"]},
        )

    def test_geosever_users_no_permission_response(self):
        user = UserFactory()
        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        privilege_response = self.privilege_geoserver_users(web_client)

        self.assertEqual(
            privilege_response.status_code,
            403,
            "User credentials response: response status code is not 403",
        )

    def test_geosever_users_response(self):
        user = UserFactory()
        user.is_staff = True
        user.save()

        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        privilege_response = self.privilege_geoserver_users(web_client)
        self.assertEqual(
            privilege_response.json(),
            {"users": [{"groups": ["free"], "username": user.username}]},
        )

    def test_geosever_users_groups_response(self):
        user = UserFactory()
        user.is_staff = True
        user.save()

        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        privilege_response = self.privilege_geoserver_users(web_client)
        self.assertAlmostEqual(
            privilege_response.json(),
            {"users": [{"groups": ["free"], "username": user.username}]},
        )

    def test_has_login_permission(self):
        user = UserFactory()
        oidc_client = OIDCConfidentialClientFactory.create()
        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        # test when the Client has no preventions registered
        has_perm, message = has_login_permission(user, oidc_client.id)
        self.assertIsNone(message)
        self.assertTrue(has_perm)

        # test when the Client has preventions of user subscription
        prevention = OpenIdLoginPreventionFactory.create(oidc_client=oidc_client)
        prevention.groups.set([GroupFactory(name=user.get_team()).id])
        has_perm, message = has_login_permission(user, oidc_client.client_id)
        self.assertEqual(
            message,
            "Your subscription does not allow this login. You need to upgrade your subscription to continue.",
        )
        self.assertFalse(has_perm)
