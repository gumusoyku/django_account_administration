from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client

from .mixins import AccountMixin, UserMixin
from .models import Account

# Info of the users who are going to be administrators
FIRST_USER_USERNAME = "first_user"
SECOND_USER_USERNAME = "second_user"
THIRD_USER_USERNAME = "third_user"

# Root user is the super user who will have all the permissions
ROOT_USER_USERNAME = "root"

TEST_USER_PASSWORD = "t3st_p4ssw0rd"

# Info of the each account that are going to be created by administrators
FIRST_ACCOUNT_FIRST_NAME = "first_account"
SECOND_ACCOUNT_FIRST_NAME = "second_account"
THIRD_ACCOUNT_FIRST_NAME = "third_account"
FOURTH_ACCOUNT_FIRST_NAME = "fourth_account"

TEST_ACCOUNT_LAST_NAME = "last_name"

# IBANs
FIRST_IBAN = "AL29682892951958427147515828"
SECOND_IBAN = "AL1094853292ZW0OMA0U17JB46XL"
THIRD_IBAN = "TR 12-1234567 1234567-12345678"
FOURTH_IBAN = "DE36000000000"


class BaseTest(AccountMixin, UserMixin, TestCase):
    """
    Users are the ones who will have restricted permissions. ie. Administrators.
    Test case:
        - first_user creates first_account
        - second_user creates second_account
        - third_user creates third_account
        - root_user creates fourth_account
    """

    def setUp(self):
        self.client = Client()
        # create test users
        self.first_user = self.create_user(username=FIRST_USER_USERNAME,
                                           password=TEST_USER_PASSWORD)
        self.second_user = self.create_user(username=SECOND_USER_USERNAME,
                                            password=TEST_USER_PASSWORD)
        self.third_user = self.create_user(username=THIRD_USER_USERNAME,
                                           password=TEST_USER_PASSWORD)
        self.root_user = self.create_user(username=ROOT_USER_USERNAME,
                                          password=TEST_USER_PASSWORD)

        self.make_user_superuser(user=self.root_user)
        self.make_user_staff(user=self.root_user)

        # create test accounts
        self.first_account = self.create_account(first_name=FIRST_ACCOUNT_FIRST_NAME,
                                                 last_name=TEST_ACCOUNT_LAST_NAME,
                                                 created_by=self.first_user,
                                                 iban=FIRST_IBAN)

        self.second_account = self.create_account(first_name=SECOND_ACCOUNT_FIRST_NAME,
                                                  last_name=TEST_ACCOUNT_LAST_NAME,
                                                  created_by=self.second_user,
                                                  iban=SECOND_IBAN)

        self.third_account = self.create_account(first_name=THIRD_ACCOUNT_FIRST_NAME,
                                                 last_name=TEST_ACCOUNT_LAST_NAME,
                                                 created_by=self.third_user,
                                                 iban=THIRD_IBAN)

        self.fourth_account = self.create_account(first_name=FOURTH_ACCOUNT_FIRST_NAME,
                                                  last_name=TEST_ACCOUNT_LAST_NAME,
                                                  created_by=self.root_user,
                                                  iban=FOURTH_IBAN)


class AccountTests(BaseTest):

    def setUp(self):
        super(AccountTests, self).setUp()
        self.give_user_permissions(user=self.first_user,
                                   permission_codenames=["add_account", "change_account", "delete_account"])

        self.make_user_staff(user=self.first_user)

    def test_user_can_delete_accounts_via_admin(self):
        # set the client's info using login
        self.client.login(username=FIRST_USER_USERNAME,
                          password=TEST_USER_PASSWORD)
        # Set change_url
        delete_url = reverse('admin:accounts_account_delete',
                             args=(self.first_account.id,))
        data = {
            "post": "yes"
        }

        response = self.client.post(delete_url, data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_cant_delete_accounts_via_admin(self):

        # set the client's info using login
        self.client.login(username=FIRST_USER_USERNAME,
                          password=TEST_USER_PASSWORD)
        # Set change_url
        delete_url = reverse('admin:accounts_account_delete',
                             args=(self.second_account.id,))
        data = {
            "post": "yes"
        }

        response = self.client.post(delete_url, data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_user_can_delete_accounts_using_action(self):
        """
        Test that an administrator user, can delete accounts that are created by them
        using admin delete_selected action.
        """
        # set the client's info using login
        self.client.login(username=FIRST_USER_USERNAME,
                          password=TEST_USER_PASSWORD)
        # Set change_url
        change_url = reverse('admin:accounts_account_changelist')

        # Set POST data to be passed to changelist url
        data = {
            'action': 'delete_selected',
            '_selected_action': self.first_account.id
        }

        self.client.post(change_url, data, follow=True)

        # since the first_account created by first_user
        # account can be deleted using delete_selected action.

        self.assertEqual(
            Account.objects.filter(id=self.first_account.id).count(), 0
        )

    def test_user_cant_delete_accounts_using_action(self):
        """
        Test that an administrator user, can not delete accounts that are created by other administrators
        using admin delete_selected action.
        """
        # set the client's info using login
        self.client.login(username=FIRST_USER_USERNAME,
                          password=TEST_USER_PASSWORD)
        # Set change_url
        change_url = reverse('admin:accounts_account_changelist')

        # Set POST data to be passed to changelist url
        data = {
            'action': 'delete_selected',
            '_selected_action': self.second_account.id
        }

        self.client.post(change_url, data, follow=True)

        # since the second_account created by second_user
        # account cant be deleted using delete_selected action.

        self.assertEqual(
            Account.objects.filter(id=self.first_account.id).count(), 1
        )

    def test_root_user_can_delete_any_account(self):
        # set the client's info using login
        self.client.login(username=ROOT_USER_USERNAME,
                          password=TEST_USER_PASSWORD)
        # Set change_url
        delete_url = reverse('admin:accounts_account_delete',
                             args=(self.first_account.id,))
        data = {
            "post": "yes"
        }

        response = self.client.post(delete_url, data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_root_user_can_delete_any_account_using_action(self):
        """
        Test that an root user, can delete any accounts.
        """
        # set the client's info using login
        self.client.login(username=ROOT_USER_USERNAME,
                          password=TEST_USER_PASSWORD)
        # Set change_url
        change_url = reverse('admin:accounts_account_changelist')

        # Set POST data to be passed to changelist url
        data = {
            'action': 'delete_selected',
            '_selected_action': self.first_account.id
        }

        self.client.post(change_url, data, follow=True)

        # since user is root, can delete any account
        self.assertEqual(
            Account.objects.filter(id=self.first_account.id).count(), 0
        )
