from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category']
    read_only_fields = ['id']
  

# class ShowProductsSerializer(serializers.ModelSerializer):

#   class Meta:
#     model = Product
#     fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category']



# class EditProductSerializer(serializers.ModelSerializer):

#   class Meta:
#     model = Product
#     fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category']


# class GetProductDetailsSerializer(serializers.ModelSerializer):

#   class Meta:
#     model = Product
#     fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category']