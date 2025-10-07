from django.db import models
from django.contrib.auth.models import User


class Meal(models.Model):
    meal_id = models.CharField(max_length=200, unique=True)
    meal_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="uploads/meals/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["meal_name"]  

    def __str__(self):
        return self.meal_name


class MenuItem(models.Model):
    menu_id = models.CharField(max_length=100)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="menu_items", null=True, blank=True)
    image = models.ImageField(upload_to="uploads/menu_items/", blank=True, null=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="menu_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"] 
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return f"{self.menu_id} ({self.vendor.username})"
