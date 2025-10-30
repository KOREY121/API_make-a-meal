from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView



class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "status": "success",
                "message": f"Registration successful. Welcome, {user.first_name or user.username}!",
                "data": {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                }
            }, status=status.HTTP_201_CREATED)

        # Error message
        return Response({
            "status": "error",
            "message": "Registration failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

