from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import CartItem, Cart

class AddToCartSerializer(serializers.ModelSerializer):

  class Meta:
    model = CartItem
    fields = ['product', 'quantity']

  def validate_quantity(self, value):

    if value <= 0:
      raise serializers.ValidationError("cart_item quantity should not be zero")
    return value
    
  def validate(self, attrs):
    product = attrs['product']
    quantity = attrs['quantity']
    request = self.context['request']

    cart = Cart.objects.filter(user=request.user).first()

    existing_quantity = 0

    if cart:
      cart_item = CartItem.objects.filter(cart=cart, product=product).first()

      if cart_item:
        existing_quantity = cart_item.quantity

    if quantity + existing_quantity > product.stock_quantity:
      raise serializers.ValidationError("Out of stock")
      
    return attrs
  
  def create(self, validated_data):
    request = self.context['request']
    product = validated_data['product']
    quantity = validated_data['quantity']

    cart, _ = Cart.objects.get_or_create(
      user=request.user
    )
    cart_item = CartItem.objects.filter(
      cart=cart,
      product=product
    ).first()

    if cart_item:
      cart_item.quantity += quantity
      cart_item.save()
    else:
      cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=quantity
      )

    return cart_item





class CartItemDisplaySerializer(serializers.ModelSerializer):

  product_id = serializers.IntegerField(source="product.id", read_only=True)
  product_name = serializers.CharField(source="product.name", read_only=True)
  price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)

  class Meta:
    model = CartItem
    fields = ['id', 'product_id', 'product_name', 'price', 'quantity', 'sub_total' ]
    read_only_fields = ['id', 'sub_total']


class CartItemUpdateSerializer(serializers.ModelSerializer):

  class Meta:
    model = CartItem
    fields = ['id', 'cart', 'product', 'quantity']
    read_only_fields = ['id', 'cart', 'product']