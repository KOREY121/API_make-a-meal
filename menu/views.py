from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Meal, MenuItem
from .serializers import MealSerializer, MenuItemSerializer

from django.http import JsonResponse

def make_a_meal_view(request):
    return JsonResponse({"message": "make a meal endpoint is working!"})


class MealViewSet(viewsets.ModelViewSet):
    
    queryset = Meal.objects.all().order_by("-created_at")
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MenuItemViewSet(viewsets.ModelViewSet):
    
    queryset = MenuItem.objects.select_related("vendor", "meal").all().order_by("-created_at")
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        
        serializer.save(vendor=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def my_menu(self, request):
        
        menu_items = MenuItem.objects.filter(vendor=request.user)
        serializer = self.get_serializer(menu_items, many=True)
        return Response(serializer.data)
