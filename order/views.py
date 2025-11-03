from django.shortcuts import render
from .serializers import OrderSerializer,CartSerializer
from .models import Order,Cart
from rest_framework.response import Response
from rest_framework import status, viewsets,permissions
from rest_framework.permissions import IsAuthenticated



from django.http import JsonResponse



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'account_profile') and user.account_profile.role == 'vendor':
            # here the vendors can only see orders that include their meals
            return self.queryset.filter(items__meal__vendor=user).distinct()
        return self.queryset.filter(customer=user)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

