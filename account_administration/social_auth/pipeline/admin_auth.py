"""
This file is for adding custom pipeline operators to social_django.
Do the admin authentication related configurations here.
"""


def set_staff_status_true(user, *args, **kwargs):
    """
    Mark the authenticated user as staff status so that they can login to admin site.
    """
    if user:
        user.is_staff = True
        user.save(update_fields=["is_staff"])
