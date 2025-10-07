from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers




user = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        
