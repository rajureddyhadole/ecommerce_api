from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return str(self.id)

class Product(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.01))])
  stock_quantity = models.PositiveIntegerField(default=0)
  category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")