from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import CartItem, Cart
from products.serializers import ProductSummarySerializer

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
  product_info = ProductSummarySerializer(source="product", read_only=True)

  class Meta:
    model = CartItem
    fields = ['id', 'product_info', 'quantity', 'sub_total' ]
    read_only_fields = ['id', 'sub_total']


class CartItemUpdateSerializer(serializers.ModelSerializer):
  quantity = serializers.IntegerField(required=True)

  class Meta:
    model = CartItem
    fields = ['quantity']

  def validate_quantity(self, quantity):

    if quantity <= 0:
      raise serializers.ValidationError("quantity should be at least 1.")
    
    existing_stock = self.instance.product.stock_quantity

    if existing_stock < quantity:
      raise serializers.ValidationError(f"Only {existing_stock} items are currently available.")
    
    return quantity
