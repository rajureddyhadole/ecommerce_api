from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category']
    read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):

  class Meta:
    model = Category
    fields = ['id', 'name']
    read_only_fields = ['id']


class ProductSummarySerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = ['id', 'name', 'price']