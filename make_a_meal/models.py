from django.db import models
from django.contrib.auth.models import User, AbstractUser


from django.contrib.auth.models import User
from django.db import models

#class Profile(models.Model):
 #   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  #  created_at = models.DateTimeField(auto_now_add=True)
   # updated_at = models.DateTimeField(auto_now=True)

    #def __str__(self):
     #   return self.user.username



class MenuItem(models.Model):
    menu_id = models.CharField(max_length=100 )
    image_url = models.FileField(upload_to="uploads/", blank=True, null=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.menu_id
    

    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)