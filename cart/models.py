from django.db import models
from products.models import Product
from django.conf import settings

# Create your models here.
class Cart(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.user)


class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)

  @property
  def sub_total(self):
    return self.product.price * self.quantity
  
