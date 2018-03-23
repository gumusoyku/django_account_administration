from django.db import models
from django.utils.translation import ugettext_lazy as _
from localflavor.generic.models import IBANField


class Account(models.Model):
    """
    Account model that holds the name fields and IBAN no of the accounts
    """
    first_name = models.CharField(_("First Name"), max_length=30)
    last_name = models.CharField(_("Last Name"), max_length=30)
    IBAN = IBANField(_("IBAN NO"), use_nordea_extensions=True)

    class Meta:
        verbose_name = _("Account")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
