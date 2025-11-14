from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer
from .models import Meal, MenuItem


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [ "name","price", "image","vendor", "date", "created_at", "updated_at"]


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
