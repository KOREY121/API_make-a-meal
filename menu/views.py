from rest_framework import viewsets, permissions,status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

from datetime import date, timedelta

from .models import Meal, MenuItem
from .serializers import MealSerializer, MenuItemSerializer

from django.http import JsonResponse


class MealViewSet(viewsets.ModelViewSet):
    
    queryset = Meal.objects.all().order_by("-created_at")
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)


    def get_queryset(self):
        user = self.request.user
        today = date.today()
        tomorrow = today + timedelta(days=1)

        # ✅ Vendors see all their meals
        if user.is_authenticated and hasattr(user, 'account_profile') and user.account_profile.role == 'vendor':
            return Meal.objects.filter(vendor=user).order_by("-created_at")

        # ✅ Customers/public only see today and tomorrow’s meals
        return Meal.objects.filter(date__in=[today, tomorrow]).order_by("-created_at")
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})

        user = request.user
        if user.is_authenticated and hasattr(user, 'account_profile') and user.account_profile.role == 'vendor':
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Custom message for customers/public users
        return Response({
            "message": "Showing only meals available for today and tomorrow.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

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
