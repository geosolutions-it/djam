from django.utils.translation import ugettext as _
from django.db.models import Q
from oidc_provider.lib.claims import ScopeClaims

from apps.privilege_manager.models import Group


class CustomScopeClaims(ScopeClaims):

    info_user_id = (
        _(u'User ID'),
        _(u'Access to your User ID number'),
    )

    def scope_user_id(self):
        dic = {
            'user_id': self.user.id,
        }

        return dic

    info_groups = (
        _(u'User Privilege Groups'),
        _(u'Access to your Privilege Groups'),
    )

    def scope_groups(self):
        dic = {
            'groups': [user_group.name for user_group in Group.objects.filter(Q(users__id=self.user.id))]
        }

        return dic
