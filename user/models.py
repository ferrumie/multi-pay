from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from .manager import CustomUserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)

    phone_number = PhoneNumberField(
        _("Phone number"), blank=True,
        help_text=_("User's phone number "))

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
