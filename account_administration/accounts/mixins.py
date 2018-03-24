from django.contrib.auth.models import User, Permission

from .models import Account


# **  Test related mixins ** #


class AccountMixin(object):
    def create_account(self, first_name, last_name, iban, created_by):
        return Account.objects.create(first_name=first_name, last_name=last_name,
                                      IBAN=iban, created_by=created_by)


class UserMixin(object):
    def create_user(self, username, password):
        return User.objects.create_user(username=username, password=password)

    def make_user_staff(self, user):
        user.is_staff = True
        user.save(update_fields=["is_staff"])

    def make_user_superuser(self, user):
        user.is_superuser = True
        user.save(update_fields=["is_superuser"])

    def give_user_permissions(self, user, permission_codenames):
        permission_list = []
        for permission_codename in permission_codenames:
            permission = Permission.objects.get(codename=permission_codename)
            permission_list.append(permission)

        user.user_permissions.set(permission_list)
