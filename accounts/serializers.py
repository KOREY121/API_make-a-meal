from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile




user = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        



class UserRegistrationSerializer(serializers.ModelSerializer):
    # these  are my fields for Profile
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, default='user')
    business_name = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "business_name",
            "address",
        ]

    def create(self, validated_data):
        role = validated_data.pop("role", "user")
        business_name = validated_data.pop("business_name", "")
        address = validated_data.pop("address", "")

        # this should create user
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )

        # Create related profile
        Profile.objects.create(
            user=user,
            role=role,
            business_name=business_name,
            address=address,
        )

        return user
