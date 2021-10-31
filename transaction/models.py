from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Transaction(models.Model):
    amount = models.DecimalField(
        _("Plan Amount"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    api_key = models.CharField(
        _('Verified'), max_length=255, unique=True)

    platform = models.CharField(
        _('Payment Platform'), max_length=150)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
