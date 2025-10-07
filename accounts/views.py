from django.http import JsonResponse
from django.shortcuts import render

def make_a_meal_view(request):
    return JsonResponse({"message": "Welcome to Make a Meal API!"})
