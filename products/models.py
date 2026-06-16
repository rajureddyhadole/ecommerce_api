from django.db import models

# Create your models here.

class Category(models.Model):
  title = models.TextField()
  description = models.TextField()


class Product(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  product = models.TextField()
  productImage = models.ImageField(null=True, blank=True)