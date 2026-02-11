from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer
from .models import Meal, MenuItem


class MealSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.username', read_only=True)
    description = serializers.CharField(required=False, allow_blank=True)
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Meal
        fields = ['id', 'name', 'price', 'image', 'description', 'date', 'vendor', 'vendor_name', 'created_at']
        read_only_fields = ['vendor', 'created_at']
    
    def get_image_url(self, obj):
        """Return full URL for image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class MenuItemSerializer(serializers.ModelSerializer):
    item_id = serializers.CharField(source="menu_id", read_only=True)
    vendor = UserSerializer(read_only=True)
    meal = MealSerializer(read_only=True)
    

    class Meta:
        model = MenuItem
        fields = [
            "item_id",
            "menu_id",
            "meal",
            "image",
            "vendor",
            "created_at",
            "updated_at",
        ]
