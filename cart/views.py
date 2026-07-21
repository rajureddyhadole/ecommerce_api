from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CartItemUpdateSerializer, AddToCartSerializer, CartItemDisplaySerializer
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

      serializer = CartItemDisplaySerializer(cart_items, many=True)

      return Response({
        'data': serializer.data
      })
    else:
      return Response({
        'message': "your cart is empty. add some products",
        'data': []
      }, status=status.HTTP_200_OK)

  

  if request.method == "POST":

    serializer = AddToCartSerializer(data=request.data, context={'request': request})

    serializer.is_valid(raise_exception=True)

    cart_item = serializer.save()

    response_serializer = CartItemDisplaySerializer(cart_item)

    return Response({
      'data': response_serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_item_detail(request, cart_item_id):

  if request.method == "PATCH":

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
  


  if request.method == "DELETE":
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if cart_item.cart.user != request.user:

      return Response({
        'error': "you are not allowed to perform this operation."
      }, status=status.HTTP_403_FORBIDDEN)
    
    cart_item.delete()

    return Response({
      'message': "cart item is successfully removed from cart."
    }, status=status.HTTP_200_OK)