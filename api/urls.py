from django.urls import path, include
from .import views
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet,CartViewSet,OrderViewSet

router = DefaultRouter()
router.register('menu-items', MenuItemViewSet, basename='menuitem')
router.register('cart', CartViewSet)
router.register('orders', OrderViewSet)


urlpatterns = [
    path('make_a_meal/', views.make_a_meal_view),


    path('', include(router.urls))
]