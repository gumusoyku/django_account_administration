from django.contrib.auth.models import User
from django.test import TestCase

from accounts.mixins import UserMixin
from accounts.tests import FIRST_USER_USERNAME, TEST_USER_PASSWORD
from .pipeline.admin_auth import set_staff_status_true
from .pipeline.permissions import set_permissions


class PipelineTests(UserMixin, TestCase):
    """
    Test the social_auth pipelines
    """

    def setUp(self):
        self.first_user = self.create_user(username=FIRST_USER_USERNAME,
                                           password=TEST_USER_PASSWORD)

    def test_set_staff_status_true_pipeline(self):
        # at first, user is not a staff user
        set_staff_status_true(user=self.first_user)
        self.assertTrue(self.first_user.is_staff)

    def test_set_permissions_pipeline(self):
        set_permissions(user=self.first_user)
        # since django caches the permissions of users,
        # fetch the user from database again.
        first_user = User.objects.get(username=FIRST_USER_USERNAME)

        self.assertTrue(first_user.has_perm("accounts.add_account"))
        self.assertTrue(first_user.has_perm("accounts.change_account"))
        self.assertTrue(first_user.has_perm("accounts.delete_account"))
