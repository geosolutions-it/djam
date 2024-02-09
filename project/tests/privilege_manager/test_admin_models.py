from unittest import skip
from unittest.mock import MagicMock, patch

from django.http import HttpRequest
from django.test import TestCase
from django.contrib import admin

from apps.identity_provider.models import ApiKey
from apps.privilege_manager.admin import GroupAdmin
from apps.privilege_manager.models import Group
from tests import UserFactory, ApiKeyFactory, GroupFactory, get_user_model


class TestAdminGroup(TestCase):
    @skip("GroupAdmin doesn't have _generate_api_key_for_enterprise_user method")
    def test_api_key_creation_invoked(self):
        g_a = GroupAdmin(Group, admin.site)
        fake_method = MagicMock()
        fake_object = MagicMock()

        attrs = {"name": Group.GroupNames.ENTERPRISE.value}
        fake_object.configure_mock(**attrs)
        with patch.object(
            GroupAdmin, "_generate_api_key_for_enterprise_user", fake_method
        ):
            g_a.save_model(HttpRequest(), fake_object, MagicMock(), MagicMock())
            self.assertTrue(fake_method.called)

    @skip("GroupAdmin doesn't have _generate_api_key_for_enterprise_user method")
    def test_api_key_not_invoked(self):
        g_a = GroupAdmin(Group, admin.site)
        fake_method = MagicMock()
        fake_object = MagicMock()

        attrs = {"name": "not_enterprise_group"}
        fake_object.configure_mock(**attrs)
        with patch.object(
            GroupAdmin, "_generate_api_key_for_enterprise_user", fake_method
        ):
            g_a.save_model(HttpRequest(), fake_object, MagicMock(), MagicMock())
            self.assertFalse(fake_method.called)

    @patch("django.contrib.admin.ModelAdmin.save_model")
    def test_users_not_passed(self, save_mock):
        group_setup = self._prepare_initial_setup()
        g_a = GroupAdmin(Group, admin.site)
        g = group_setup.get("g")
        # no users in changed data
        fake_form = MagicMock()
        with patch(
            "apps.identity_provider.models.ApiKey.objects.create"
        ) as create_mock, patch(
            "apps.identity_provider.models.ApiKey.objects.filter"
        ) as filter_mock:
            g_a.save_model(HttpRequest(), g, fake_form, MagicMock())
            self.assertFalse(create_mock.called)
            self.assertFalse(filter_mock.called)

    @patch("django.contrib.admin.ModelAdmin.save_model")
    def test_nothing_to_change_assignment(self, create_mock):
        group_setup = self._prepare_initial_setup()
        g_a = GroupAdmin(Group, admin.site)
        # no users in changed data
        fake_form = MagicMock()
        g = group_setup.get("g")
        with patch(
            "apps.identity_provider.models.ApiKey.objects.create"
        ) as create_mock, patch(
            "apps.identity_provider.models.ApiKey.objects.filter"
        ) as filter_mock:
            g_a.save_model(HttpRequest(), g, fake_form, MagicMock())
            self.assertFalse(create_mock.called)
            self.assertFalse(filter_mock.called)

    @skip("Model Group doesn't have anymore the users connection")
    def test_add_new_user(self):
        initial_ak_count = 3
        group_setup = self._prepare_initial_setup()
        g_a = GroupAdmin(Group, admin.site)
        # no users in changed data
        fake_form = MagicMock()
        g = group_setup.get("g")
        g.users.add(UserFactory())
        fake_form.configure_mock(
            changed_data=["users"],
            cleaned_data={"users": g.users.all()},
            initial={"users": [ud.get("u") for ud in group_setup.get("users")]},
        )

        g_a.save_model(HttpRequest(), g, fake_form, MagicMock())
        self.assertGreater(ApiKey.objects.all().count(), initial_ak_count)

    @skip("Model Group doesn't have anymore the users connection")
    def test_remove_user(self):
        group_setup = self._prepare_initial_setup()
        g_a = GroupAdmin(Group, admin.site)
        # no users in changed data
        fake_form = MagicMock()
        g = group_setup.get("g")
        u = group_setup.get("users")[0].get("u")
        g.users.remove(group_setup.get("users")[0].get("u"))
        fake_form.configure_mock(
            changed_data=["users"],
            cleaned_data={"users": g.users.all()},
            initial={"users": [ud.get("u") for ud in group_setup.get("users")]},
        )

        g_a.save_model(HttpRequest(), g, fake_form, MagicMock())
        self.assertTrue(ApiKey.objects.get(user=u).revoked)

    def _prepare_initial_setup(self):
        u1 = UserFactory()
        u2 = UserFactory()
        u3 = UserFactory()
        a1 = ApiKeyFactory(user=u1)
        a2 = ApiKeyFactory(user=u2)
        a3 = ApiKeyFactory(user=u3)

        g = GroupFactory(name="enterprise")
        return {
            "group": g,
            "users": [{"u": u1, "ak": a1}, {"u": u2, "ak": a2}, {"u": u3, "ak": a3}],
        }
