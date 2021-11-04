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
            # if email exist raise error
            raise serializers.ValidationError(
                "A user with this email allready exists")
        
        # Verify the password
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError("Passwords do not match")

        try:
            # Validate password
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
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserApiKey
        fields = '__all__'


class ChoiceField(serializers.ChoiceField):
    '''
    Override the default ChoiceField, to make
    it return a list of value and its property
    instead of returning just the value
    '''

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if key == data:
                return [key, val]
        self.fail('invalid_choice', input=data)


class PaymentSerializer(serializers.Serializer):
    PAYMENT_CHOICES = (
        ('PAYPAL', 'paypal'),
        ('PAYSTACK', 'paystack'),
        ('STRIPE', 'stripe'),
        ('FLUTTERWAVE', 'rave_payment'),
        ('COINBASE', 'coinbase')

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
    platform = ChoiceField(choices=PAYMENT_CHOICES)
    title = serializers.CharField(
        max_length=255, required=False)
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    currency = serializers.ChoiceField(
        choices=CURRENCY_CHOICES, default='NGN')
    logo = serializers.URLField(required=False)


class PaymentConfirmSerializer(serializers.Serializer):
    PAYMENT_CHOICES = (
        ('PAYPAL', 'paypal'),
        ('PAYSTACK', 'paystack'),
        ('STRIPE', 'stripe'),
        ('FLUTTERWAVE', 'rave_payment'),
        ('CRYPTO', 'crypto')

    )

    platform = ChoiceField(choices=PAYMENT_CHOICES, required=False)


class MyAuthTokenSerializer(serializers.Serializer):
    '''
    Override the default auth serializer
    to take in email and password to retrieve token instead of using username
    '''
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
