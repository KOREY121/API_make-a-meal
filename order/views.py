from django.shortcuts import render
from .serializers import OrderSerializer,CartSerializer
from .models import Order,Cart, OrderItem
from rest_framework.response import Response
from rest_framework import status, viewsets,permissions
from rest_framework.permissions import IsAuthenticated
from django.db import transaction






class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user

        # this gets user active cart
        try:
            cart = Cart.objects.get(user=user, is_active=True)
        except Cart.DoesNotExist:
            return Response({"detail": "Your cart is empty."},
                            status=status.HTTP_400_BAD_REQUEST)

        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({"detail": "Your cart has no items."},
                            status=status.HTTP_400_BAD_REQUEST)

        vendor = cart_items.first().menu_item.vendor  

        # this creates an order
        order = Order.objects.create(
            id=str(user.id) + "-ORDER",    
            customer_id=user,
            vendor_id=vendor,
            price=0,
            total_amount=0,
            payment_status="pending",
        )

        total = 0

        
        for item in cart_items:
            line_total = item.menu_item.price * item.quantity

            OrderItem.objects.create(
                order_id=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                price=line_total,
            )

            total += line_total

        # Update order total
        order.total_amount = total
        order.price = total
        order.save()

        # this deactivates cart like you instructed sir
        cart.is_active = False
        cart.save()

        return Response(OrderSerializer(order).data,
                        status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'account_profile') and user.account_profile.role == 'vendor':
            # here the vendors can only see orders that include their meals
            return self.queryset.filter(vendor_id=user).distinct()
        return self.queryset.filter(customer_id=user)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

