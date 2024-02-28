from typing import Any
from django.db import models

from django.contrib.auth.models import User
from uuid import uuid4


# Create your models here.

class Collection(models.Model):
    name=models.CharField(max_length=100)
    featured_product=models.ForeignKey("Product",on_delete=models.SET_NULL,null=True, blank=True, related_name="+")

    def __str__(self):
        return self.name.capitalize()
        

class Product(models.Model):
    name= models.CharField(max_length=255)
    unit_price= models.DecimalField(max_digits=8, decimal_places=2)
    inventory=models.PositiveIntegerField()
    description=models.TextField()
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT)


    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image/store/products", null=True, blank=True)    



class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4) 
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)




class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


ODER_STATUS_PENDING="p"
ODER_STATUS_COMPLETE="c"
ODER_STATUS_FAILED="f"


ODER_STATUS_CHOICES=[
    (ODER_STATUS_PENDING,"Pending"),
    (ODER_STATUS_COMPLETE,"Complete"),
    (ODER_STATUS_FAILED,"failed"),
]


class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True)
    status =  models.CharField(max_length=1, default=ODER_STATUS_PENDING, choices=ODER_STATUS_CHOICES)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity= models.PositiveIntegerField()

