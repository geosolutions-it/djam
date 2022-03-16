from django.db.models import ObjectDoesNotExist
from apps.privilege_manager.models import Group, OpenIdLoginPrevention


def has_login_permission(user, oidc_client_id):
    """
    Function checking User's OIDC login permission to a certain client.

    Function body is adapting RBAC authorization based on User's privilege Groups.
    To be changed when permission system is introduced.
    :param user: User model instance of an authenticated user
    :param oidc_client_id: OIDC Client's id
    :return: tuple(bool, string) -> flag determining whether the user has login permission and error message, in case they don't
    """

    try:
        preventions = OpenIdLoginPrevention.objects.get(
            oidc_client__client_id=oidc_client_id
        )
    except ObjectDoesNotExist:
        # if the Client has no preventions registered, allow login
        return True, None

    all_permission_groups = Group.objects.all()

    groups_allowed = all_permission_groups.difference(preventions.groups.all())
    user_group = user.get_group()

    has_permission = False
    if user_group in groups_allowed.values_list('name', flat=True):
        has_permission = True

    message = (
        "Your subscription does not allow this login. You need to upgrade your subscription to continue."
        if not has_permission
        else None
    )

    return has_permission, message
