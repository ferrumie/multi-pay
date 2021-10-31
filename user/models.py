from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from .manager import CustomUserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    username = None
    email = models.EmailField(_('Email Address'), unique=True)

    phone_number = PhoneNumberField(
        _("Phone number"), blank=True,
        help_text=_("User's phone number "))

    is_verified = models.BooleanField(
        _('Verified'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'verified. Default is False`'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserApiKey(models.Model):
    """Model for adding api key for different payment platforms"""

    PAYMENT_CHOICES = (
        ('PAYPAL', 'paypal'),
        ('PAYSTACK', 'paystack'),
        ('STRIPE', 'stripe'),
        ('FLUTTERWAVE', 'rave_payment'),
        ('CRYPTO', 'crypto')

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.CharField(
        _('Api Key'), max_length=255)
    platform = models.CharField(
        _('Payment Platform'), max_length=15,
        choices=PAYMENT_CHOICES)
