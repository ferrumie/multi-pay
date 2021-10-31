from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

from transaction.models import Transaction
from user.models import UserApiKey

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for user registeration"""
    password = serializers.CharField(
        max_length=255,
        required=True,
        style={"input_type": "password"},
        write_only=True
    )
    password2 = serializers.CharField(
        max_length=255,
        required=True,
        style={"input_type": "password"},
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'phone_number', 'password', 'password2']

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                "A user with this email allready exists")
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError("Passwords do not match")

        try:
            password_validation.validate_password(attrs["password"])
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApiKey
        fields = '__all__'


class PaymentSerializer(serializers.Serializer):
    PAYMENT_CHOICES = (
        ('PAYPAL', 'paypal'),
        ('PAYSTACK', 'paystack'),
        ('STRIPE', 'stripe'),
        ('rave_payment', 'rave_payment'),
        ('CRYPTO', 'crypto')

    )
    CURRENCY_CHOICES = (
        ('NGN', 'ngn'),
        ('USD', 'usd'),
        ('EUR', 'eur'),
        ('CAD', 'cad'),
        ('BTC', 'btc')

    )
    description = serializers.CharField(
        max_length=255, required=False)
    platform = serializers.ChoiceField(choices=PAYMENT_CHOICES)
    title = serializers.CharField(
        max_length=255, required=False)
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    currency = serializers.ChoiceField(
        choices=CURRENCY_CHOICES, default='NGN')
    logo = serializers.URLField(required=False)


class MyAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password",),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
