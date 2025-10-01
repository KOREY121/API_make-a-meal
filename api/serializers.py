from rest_framework import serializers
from make_a_meal.models import MenuItem
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from make_a_meal.models import Order,Cart,OrderItem,CartItem

user = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        

 


class MenuItemSerializer(serializers.ModelSerializer):
    item_id = serializers.SerializerMethodField()
    vendor = UserSerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ["item_id", "id", "menu_id", "image_url", "vendor", "created_at", "updated_at"]

    def get_item_id(self, obj):
        return {
            "id": obj.id,
            "image_url": obj.image_url.url if obj.image_url else None,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "order_date", "status", "total_amount", "items"]


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]

    def get_items(self, obj):
        return [
            {
                "id": item.id,
                "menu_item": item.menu_item.id,   
                "quantity": item.quantity,
            }
            for item in obj.items.all()
        ]

