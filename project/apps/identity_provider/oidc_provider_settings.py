from django.utils.translation import ugettext as _
from oidc_provider.lib.claims import ScopeClaims


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
