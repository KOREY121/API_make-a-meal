from rest_framework import serializers
from .models import Order,OrderItem
from menu.serializers import MenuItemSerializer
from accounts.serializers import UserSerializer
from .models import Cart, CartItem
from menu.models import Meal



class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    meal_id = serializers.PrimaryKeyRelatedField(
        queryset=Meal.objects.all(), source='meal', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(source='customer_id', read_only=True)
    vendor = UserSerializer(source='vendor_id', read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer","vendor", "order_date", "status", "total_amount", "items"]


    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total = 0

        for item_data in items_data:
            meal = item_data['meal']
            quantity = item_data.get('quantity', 1)
            price = meal.price * quantity
            OrderItem.objects.create(order=order, meal=meal, quantity=quantity, price=price)
            total += price

        order.total_amount = total
        order.save()
        return order
    
class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=CartItem._meta.get_field('menu_item').remote_field.model.objects.all(),
        source='menu_item',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ["id", "menu_item", "menu_item_id", "quantity", "price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]
        read_only_fields =['user']

    def get_items(self, obj):
        return [
            {
                "id": item.id,
                "menu_item": item.menu_item.id,   
                "quantity": item.quantity,
            }
            for item in obj.items.all()
        ]