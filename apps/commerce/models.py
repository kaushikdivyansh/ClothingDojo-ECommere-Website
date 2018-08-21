from __future__ import unicode_literals
from django.db import models

class Product(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255)

class Location(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    address = models.CharField(max_length=255)
    zip_code = models.IntegerField()

class Size(models.Model):
    size = models.CharField(max_length=255)

class User(models.Model):
    email = models.CharField(max_length=255)
    free = models.BooleanField()
    location = models.ForeignKey(Location, related_name='user_locations')

class Cart(models.Model):
    product = models.ForeignKey(Product, related_name='cart_products')
    size = models.ForeignKey(Size, related_name='cart_sizes')
    quantity = models.IntegerField()
    user = models.ForeignKey(User, related_name='cart_users')
    location = models.ForeignKey(Location, related_name='cart_locations')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Order(models.Model):
    user = models.ForeignKey(User, related_name='order_users')
    locked = models.BooleanField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Purchase(models.Model):
    product = models.ForeignKey(Product, related_name='purchase_products')
    size = models.ForeignKey(Size, related_name='purchase_sizes')
    quantity = models.IntegerField()
    user = models.ForeignKey(User, related_name='purchase_users')
    location = models.ForeignKey(Location, related_name='purchase_locations')
    order = models.ForeignKey(Order, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Cancellation(models.Model):
    user = models.ForeignKey(User, related_name='cancellation_users')
    order_created_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)