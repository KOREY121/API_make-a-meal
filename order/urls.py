from django.urls import path, include
from .import views
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CartViewSet

router = DefaultRouter()
router.register('cart', CartViewSet, basename= 'cart')
router.register('orders', OrderViewSet, basename= 'order')


urlpatterns = [
    path('make_a_meal/', views.make_a_meal_view),


    path('', include(router.urls))
]