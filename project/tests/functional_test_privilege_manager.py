import re
from unittest import skip

from django.test import TestCase, Client

from apps.privilege_manager.models import Group

from tests.factories.user_management_factory import UserFactory


class PrivilegeManagerBaseTestCase(TestCase):

    def privilege_geoserver_roles(self, web_client: Client):
        return web_client.get(
            '/api/privilege/geoserver/roles',
        )

    def privilege_geoserver_users(self, web_client: Client):
        return web_client.get(
            '/api/privilege/geoserver/users',
        )


class TestPrivelegeManager(PrivilegeManagerBaseTestCase):

    def test_geosever_roles_response(self):
        user = UserFactory()
        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        privilege_response = self.privilege_geoserver_roles(web_client)
        self.assertEqual(
            privilege_response.json(),
            {'groups': ['free', 'pro', 'enterprise', 'hub', 'admin']}
        )

    def test_geosever_users_no_permission_response(self):
        user = UserFactory()
        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        privilege_response = self.privilege_geoserver_users(web_client)

        self.assertEqual(privilege_response.status_code, 403, "User credentials response: response status code is not 403")

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
            {'users': [{'groups': ['free'], 'username': user.username}]}
        )

    def test_geosever_users_groups_response(self):
        user = UserFactory()
        user.is_staff = True
        user.save()

        Group.objects.get(name='pro').users.add(user)

        web_client = Client()

        # force web client's login
        web_client.force_login(user)

        privilege_response = self.privilege_geoserver_users(web_client)
        self.assertEqual(
            privilege_response.json(),
            {'users': [{'groups': ['free', 'pro'], 'username': user.username}]}
        )
