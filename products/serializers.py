from rest_framework import serializers
from .models import Product

class CreateProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category']

    extra_kwargs = {
      'category': {'read_only': True}
    }

  def create(self, validated_data):

    product = Product.objects.create(
      name=validated_data['name'],
      description=validated_data['description'],
      price=validated_data['price'],
      stock_quantity=validated_data['stock_quantity'],
      category=self.context['category']
    )

    return product
  
