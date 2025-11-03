from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from .models import Meal, MenuItem
from .serializers import MealSerializer, MenuItemSerializer

from django.http import JsonResponse


class MealViewSet(viewsets.ModelViewSet):
    
    queryset = Meal.objects.all().order_by("-created_at")
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'account_profile') and user.account_profile.role == 'vendor':
            serializer.save(vendor=user)
        else:
            raise PermissionDenied("Only vendors can create meals.")

    def perform_update(self, serializer):
        user = self.request.user
        if hasattr(user, 'account_profile') and user.account_profile.role == 'vendor':
            serializer.save()
        else:
            raise PermissionDenied("Only vendors can update meals.")

    def perform_destroy(self, instance):
        user = self.request.user
        if hasattr(user, 'account_profile') and user.account_profile.role == 'vendor':
            instance.delete()
        else:
            raise PermissionDenied("Only vendors can delete meals.")
        
    #def get_permissions(self):
    #    if self.action in ['list', 'retrieve']:
    #        permission_classes = [permissions.AllowAny]  # public access
    #    else:
    #        permission_classes = [permissions.IsAuthenticated]
    #    return [permission() for permission in permission_classes]


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
