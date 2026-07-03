from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CartItemSerializer, CartItemUpdateSerializer
from products.models import Product
from .models import Cart, CartItem
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def cart_items_list_create(request):

  if request.method == "GET":
    cart = Cart.objects.filter(user=request.user).first()

    if cart:

      cart_items = CartItem.objects.filter(cart=cart)

      serializer = CartItemSerializer(cart_items, many=True)

      return Response({
        'data': serializer.data
      })
    else:
      return Response({
        'message': "your cart is empty. add some products",
        'data': []
      }, status=status.HTTP_200_OK)

  

  if request.method == "POST":

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
                'product_id': cart_item.product.id,
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


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_cart_item_quantity(request, cart_item_id):

  cart_item = get_object_or_404(CartItem, id=cart_item_id)

  if cart_item.cart.user != request.user:

    return Response({
      'error': "You don't have the permission."
    }, status=status.HTTP_403_FORBIDDEN)
  
  serializer = CartItemUpdateSerializer(cart_item, data=request.data, partial=True)

  if serializer.is_valid():

    quantity = serializer.validated_data.get('quantity')

    if quantity == 0:

      cart_item.delete()

      return Response({
        'message': "the cartitem is removed from the cart"
      })

    if cart_item.product.stock_quantity >= quantity:

      serializer.save()

      return Response({
        'message': "quantity updated successfully",
        'data': serializer.data
      }, status=status.HTTP_200_OK)
    else:
      return Response({
        'error': "out of stock."
      }, status=status.HTTP_400_BAD_REQUEST)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

