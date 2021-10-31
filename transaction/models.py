from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Transaction(models.Model):
    amount = models.DecimalField(
        _("Plan Amount"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    platform = models.CharField(
        _('Payment Platform'), max_length=150)

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    status = models.CharField(max_length=50, blank=True)

    payment_type = models.CharField(
        _('Payment Type'), max_length=50, blank=True
    )

    account_id = models.CharField(max_length=50, blank=True)

    transaction_id = models.CharField(max_length=50, blank=True)

    transaction_ref = models.CharField(max_length=250, blank=True)

    date_created = models.DateTimeField(_('Date Created'), blank=True, null=True)
