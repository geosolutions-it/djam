from django.test import TestCase

from apps.billing.admin import CompanyAdminForm

from tests.factories.user_management_factory import UserFactory, CompanyFactory


class TestCompanyAdminForm(TestCase):

    def test_add_users_without_company(self):
        user1 = UserFactory()
        company = CompanyFactory()
        form = CompanyAdminForm(
            data={
                "company_name": "Test",
                "users": [user1]
            }, instance=company)

        self.assertEqual(form.errors, {})

    def test_add_users_with_company(self):
        user1 = UserFactory()
        user2 = UserFactory()
        company = CompanyFactory()
        company2 = CompanyFactory()
        company.users.add(user1)
        form = CompanyAdminForm(
            data={
                "company_name": "Test",
                "users": [user1, user2]
            }, instance=company2)

        self.assertEqual(
            form.errors['__all__'][0],
            f"The following users already belong to another company, Select users who are not connected to any company yet: {[user1.email]}"
        )

    def test_create_company_without_users(self):
        form = CompanyAdminForm(
            data={
                "company_name": "Test create"
            })
        self.assertEqual(form.errors, {})

    def test_create_company_with_users(self):
        user1 = UserFactory()
        user2 = UserFactory()
        company = CompanyFactory()
        company.users.add(user1)
        form = CompanyAdminForm(
            data={
                "company_name": "Test",
                "users": [user1, user2]
            })

        self.assertEqual(
            form.errors['__all__'][0],
            f"The following users already belong to another company, Select users who are not connected to any company yet: {[user1.email]}"
        )
