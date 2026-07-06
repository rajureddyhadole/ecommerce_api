from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

# Create your models here.
class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
  shipping_address = models.TextField(max_length=400)

  class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    
  payment_status = models.CharField(choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)



class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
  quantity = models.PositiveIntegerField(default=1)
  bought_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
  
  class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    RETURNED = 'returned', 'Returned'

  status = models.CharField(choices=Status.choices, default=Status.PENDING)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)