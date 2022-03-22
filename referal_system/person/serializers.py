"""person application Serializers"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


User = get_user_model()


class UserGetCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()


class UserAuthorizeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    code = serializers.CharField()


class ImplementInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                'invite_code',
        ]

    # check empty
    def validate_invite_code(self, invite_code):
        if invite_code:
            return invite_code
        else:
            raise serializers.ValidationError("field can't be empty")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                'phone_number',
                'invite_code',
                'invited_phones',
                'foreign_invite_code'
        ]
