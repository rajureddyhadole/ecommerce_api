from rest_framework import serializers
from .models import CartItem

class AddToCartSerializer(serializers.ModelSerializer):

  class Meta:
    model = CartItem
    fields = ['product', 'quantity']


class CartItemDisplaySerializer(serializers.ModelSerializer):

  product_id = serializers.IntegerField(source="product.id", read_only=True)
  product_name = serializers.CharField(source="product.name", read_only=True)
  price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)

  class Meta:
    model = CartItem
    fields = ['id', 'product_id', 'product_name', 'price', 'quantity', 'sub_total' ]


class CartItemUpdateSerializer(serializers.ModelSerializer):

  class Meta:
    model = CartItem
    fields = ['id', 'cart', 'product', 'quantity']
    read_only_fields = ['id', 'cart', 'product']