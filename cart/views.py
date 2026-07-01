from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CartItemSerializer
from products.models import Product
from .models import Cart, CartItem
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):

  serializer = CartItemSerializer(data=request.data)

  if serializer.is_valid():
    product = serializer.validated_data.get('product')
    quantity = serializer.validated_data.get('quantity')

    if product.stock_quantity >= quantity:

      cart, _ = Cart.objects.get_or_create(user=request.user)

      cart_item = CartItem.objects.filter(cart=cart, product=product).first()

      if cart_item:
        if product.stock_quantity >= (cart_item.quantity + quantity):
          cart_item.quantity += quantity
          cart_item.save()

          return Response({
            'message': "added to the cart successfully",
            'data': {
              'cart': cart_item.cart.id,
              'product_id': cart_item.id,
              'product': cart_item.product.name,
              'quantity': cart_item.quantity
            }
          })
        else:
          return Response({
            'error': "out of stock. we dont have the quantity you require"
          }, status=status.HTTP_400_BAD_REQUEST)
      else:
        cart_item_obj = CartItem.objects.create(
          cart=cart,
          product=product,
          quantity=quantity
        )

        return Response({
          'message': "cartItem created successfully",
          'data': {
            'cart': cart_item_obj.cart.id,
            'product_id': cart_item_obj.id,
            'product': cart_item_obj.product.name,
            'quantity': cart_item_obj.quantity
          }
        })
    return Response({
      'error': "out of stock."
    }, status=status.HTTP_400_BAD_REQUEST)
  else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      