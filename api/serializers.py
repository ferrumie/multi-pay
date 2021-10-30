from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

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
