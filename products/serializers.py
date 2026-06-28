from rest_framework import serializers
from .models import Product

class CreateProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category']


  def create(self, validated_data):

    product = Product.objects.create(
      name=validated_data['name'],
      description=validated_data['description'],
      price=validated_data['price'],
      stock_quantity=validated_data['stock_quantity'],
      category=validated_data['category']
    )

    return product
  

class ShowProductsSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category']



class EditProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category']


class GetProductDetailsSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category']