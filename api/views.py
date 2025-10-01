from django.shortcuts import render
from django.http import JsonResponse
from make_a_meal.models import MenuItem
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer
from make_a_meal.models import MenuItem, Cart, Order
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from django.http import JsonResponse

"""""

@api_view(['GET', 'POST'])
def make_a_mealView(request):
    if request.method == 'GET':
        meal = MenuItem.objects.all()
        serializer = MenuItemSerializer(meal, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method =='POST':
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


def make_a_meal_view(request):
    return JsonResponse({"message": "Welcome to Make a Meal API!"})



class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def perform_create(self, serializer):
        serializer.save(vendor= self.request.user)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
