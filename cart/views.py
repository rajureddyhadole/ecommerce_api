from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CartItemUpdateSerializer, AddToCartSerializer, CartItemDisplaySerializer
from .models import Cart, CartItem
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def cart_items_list_create(request):

  if request.method == "GET":
    cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')

    serializer = CartItemDisplaySerializer(cart_items, many=True)

    return Response({
      'data': serializer.data
    })


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

    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    serializer = CartItemUpdateSerializer(cart_item, data=request.data)

    serializer.is_valid(raise_exception=True)

    cart_item = serializer.save()

    response_serializer = CartItemDisplaySerializer(cart_item)

    return Response({
      'message': "quantity updated successfully",
      'data': response_serializer.data
    }, status=status.HTTP_200_OK)
  


  if request.method == "DELETE":
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    
    cart_item.delete()

    return Response({
      'message': "cart item is successfully removed from cart."
    }, status=status.HTTP_200_OK)