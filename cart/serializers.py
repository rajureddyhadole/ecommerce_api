from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):

  class Meta:
    model = CartItem
    fields = ['id', 'cart', 'product', 'quantity']
    read_only_fields = ['id', 'cart']


class CartItemUpdateSerializer(serializers.ModelSerializer):

  class Meta:
    model = CartItem
    fields = ['id', 'cart', 'product', 'quantity']
    read_only_fields = ['id', 'cart', 'product']