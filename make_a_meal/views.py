from django.shortcuts import render

from django.http import HttpResponse

def make_a_meal(request):
    return HttpResponse("<h1>Welcome to Make a Meal API 🚀</h1>")

