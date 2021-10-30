from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for user registeration"""
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'phone_number']

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                "A user with this email allready exists")
        return attrs
