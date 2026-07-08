from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderDisplaySerializer
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):

  serializer = CreateOrderSerializer(data=request.data)

  if serializer.is_valid():

    cart = get_object_or_404(Cart, user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
      return Response({
        'error': "the cart is empty"
      }, status=status.HTTP_400_BAD_REQUEST)
    
    total = 0
    for item in cart_items:

      if item.product.stock_quantity < item.quantity:
        return Response({
          'error': "out of stock"
        }, status=status.HTTP_400_BAD_REQUEST)
      
      total += item.sub_total

    
    order = Order.objects.create(
      user=request.user,
      total_amount=total,
      shipping_address =serializer.validated_data.get('shipping_address'),
      payment_status='pending'
    )

    for item in cart_items:

      OrderItem.objects.create(
        order=order,
        product=item.product,
        quantity=item.quantity,
        bought_price=item.product.price,
        status='pending'
      )

      item.product.stock_quantity -= item.quantity

      item.product.save()
    
    cart_items.delete()

    response_serializer = OrderDisplaySerializer(order)

    return Response({
      'message': "Order placed successfully",
      'data': response_serializer.data
    }, status=status.HTTP_201_CREATED)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


