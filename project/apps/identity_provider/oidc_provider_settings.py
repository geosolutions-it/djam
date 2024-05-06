from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from oidc_provider.lib.claims import ScopeClaims

from apps.privilege_manager.models import Team


class CustomScopeClaims(ScopeClaims):

    info_user_id = (
        _(u"User ID"),
        _(u"Access to your User ID number"),
    )

    def scope_user_id(self):
        dic = {
            "user_id": self.user.id,
        }

        return dic

    info_groups = (
        _(u"User Privilege Groups"),
        _(u"Access to your Privilege Groups"),
    )

    def scope_groups(self):
        dic = {"groups": [self.user.get_group()]}

        return dic

    info_legacy_user = (
        _(u"Legacy user ID"),
        _(u"Pre DJAM user id. Used to match accounts"),
    )

    def scope_legacy_user_id(self):
        User = get_user_model()
        dic = {"legacy_user_id": User.objects.get(pk=self.user.id).legacy_user_id}
        return dic

    info_is_admin = (
        _(u"Admin flag"),
        _(u"Tells if user is djam admin"),
    )

    def scope_is_admin(self):
        dic = {
            "is_admin": self.user.is_superuser,
        }

        return dic

    info_is_staff = (
        _(u"Staff flag"),
        _(u"Tells if user is djam staff member"),
    )

    def scope_is_staff(self):
        dic = {
            "is_staff": self.user.is_staff,
        }

        return dic

    info_email = (
        _(u"User email"),
        _(u"Used to update user profile data"),
    )

    def scope_email(self):
        dic = {"email": self.user.email}

        return dic
