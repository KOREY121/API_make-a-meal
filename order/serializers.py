from rest_framework import serializers
from make_a_meal.models import Order,OrderItem
from menu.serializers import MenuItemSerializer
from accounts.serializers import UserSerializer
from .models import Cart



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