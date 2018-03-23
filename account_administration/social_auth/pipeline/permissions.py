"""
This file is for adding custom pipeline operators to social_django.
Do the permission related configurations here.
"""
from django.contrib.auth.models import Permission


def set_permissions(user, *args, **kwargs):
    """
    All the authenticated users have add, change and delete permissions.
    """
    if user:
        if not user.has_perm('accounts.add_account'):
            permission_add_account = Permission.objects.get(codename="add_account")
            user.user_permissions.add(permission_add_account)
        if not user.has_perm('accounts.change_account'):
            permission_change_account = Permission.objects.get(codename="change_account")
            user.user_permissions.add(permission_change_account)
        if not user.has_perm('accounts.delete_account'):
            permission_delete_account = Permission.objects.get(codename="delete_account")
            user.user_permissions.add(permission_delete_account)
