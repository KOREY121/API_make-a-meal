from django.shortcuts import render
from .serializers import OrderSerializer,CartSerializer
from .models import Order,Cart
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated



from django.http import JsonResponse

def make_a_meal_view(request):
    return JsonResponse({"message": "Make a meal endpoint is working!"})





class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

