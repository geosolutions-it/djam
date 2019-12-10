from oauth2_provider import views
from django.contrib.auth.mixins import UserPassesTestMixin

# Views in this file are overridden in order to have a custom login screen, instead of django admin auth view,
# which is default for staff_member_required


class IsStaffProtectedApplicationList(views.ApplicationList, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class IsStaffProtectedApplicationRegistration(views.ApplicationRegistration, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class IsStaffProtectedApplicationDetail(views.ApplicationDetail, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class IsStaffProtectedApplicationDelete(views.ApplicationDelete, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class IsStaffProtectedApplicationUpdate(views.ApplicationUpdate, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class IsStaffProtectedAuthorizedTokensListView(views.AuthorizedTokensListView, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class IsStaffProtectedAuthorizedTokenDeleteView(views.AuthorizedTokenDeleteView, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
