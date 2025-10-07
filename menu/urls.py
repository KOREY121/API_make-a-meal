from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealViewSet, MenuItemViewSet, make_a_meal_view 

router = DefaultRouter()
router.register(r"meals", MealViewSet, basename="meals")
router.register(r"menu-items", MenuItemViewSet, basename="menu-items")


urlpatterns = [
    path('make_a_meal/', make_a_meal_view),


    path('', include(router.urls))
]