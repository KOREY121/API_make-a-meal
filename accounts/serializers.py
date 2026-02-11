from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    business_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "business_name"]
    
    def get_role(self, obj):
        """Safely get role, return 'user' if profile doesn't exist"""
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.role
        return 'user'  # default role
    
    def get_business_name(self, obj):
        """Safely get business_name"""
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.business_name
        return ''


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Profile fields
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, default='user')
    business_name = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=8)

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

    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        """Ensure username is unique"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        role = validated_data.pop("role", "user")
        business_name = validated_data.pop("business_name", "")
        address = validated_data.pop("address", "")

        # Create user
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