import uuid
from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    order_no = models.CharField(max_length=20, unique=True, null=True)
    customer_name = models.CharField(max_length=100)
    table_number = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    subtotal = models.DecimalField(max_digits=6,decimal_places=2,null=True)

    def __str__(self):
        return f"Order No: {self.order_no} - Customer: {self.customer_name} -Total Amount: {self.subtotal}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    menu_item_name = models.CharField(max_length=100,default="")
    menu_item_quantity = models.IntegerField(default=0)
    item_amount = models.DecimalField(max_digits=6, decimal_places=2,default=0)

    def __str__(self):
        return f"Item Name: {self.menu_item_name} - Quantity: {self.menu_item_quantity} - Order No: {self.order}"
