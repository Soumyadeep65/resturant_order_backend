# orders/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

class OptionList(models.Model):
    name = models.CharField(max_length=100)
    selection_type = models.CharField(max_length=50)  # "must_select_one" or "can_select_multiple_or_none"
    product = models.ForeignKey(Product, related_name='option_lists', on_delete=models.CASCADE)

class Option(models.Model):
    name = models.CharField(max_length=100)
    surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    option_list = models.ForeignKey(OptionList, related_name='options', on_delete=models.CASCADE)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    options = models.ManyToManyField(Option)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2)
    tip = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
