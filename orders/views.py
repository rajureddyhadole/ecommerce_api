from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from cart.models import Cart, CartItem
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderDisplaySerializer, DisplayOrdersListSerializer, ViewAllOrdersSerializer, ViewOrderDetailsSerializer, UpdateOrderItemStatusSerializer
from django.db import transaction
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

    with transaction.atomic():
    
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



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_history(request):

  orders = Order.objects.filter(user=request.user)
  
  serializer = DisplayOrdersListSerializer(orders, many=True)

  return Response({
    'message': "your order history",
    'data': serializer.data
  })

  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_details(request, order_id):

  order = get_object_or_404(Order, id=order_id, user=request.user)

  serializer = OrderDisplaySerializer(order)

  return Response({
    'message': "your order details.",
    'data': serializer.data
  })



########################## admin apis ###################

@api_view(['GET'])
@permission_classes([IsAdminUser])
def view_all_orders(request):

  orders = Order.objects.all()

  serializer = ViewAllOrdersSerializer(orders, many=True)

  return Response({
    'message': "orders list",
    'data': serializer.data
  })



@api_view(['GET'])
@permission_classes([IsAdminUser])
def view_order_details(request, order_id):
  
  order = get_object_or_404(Order, id=order_id)

  serializer = ViewOrderDetailsSerializer(order)

  return Response({
    'data': serializer.data
  })



@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_order_item_status(request, order_item_id):

  order_item = get_object_or_404(OrderItem, id=order_item_id)

  serializer = UpdateOrderItemStatusSerializer(order_item, data=request.data, partial=True)

  if serializer.is_valid():

    serializer.save()

    return Response({
      'message': "order Item status updated successfully",
      'data': serializer.data
    }, status=status.HTTP_200_OK)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



########### payment mock ##############
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay(request, order_id):

  order = get_object_or_404(Order, id=order_id, user=request.user)

  if order.PaymentStatus.PENDING:
    result = request.data.get('result', None)

    if result:
      if result == "success":
        order.payment_status = 'paid'
        order.save()

        response_serializer = DisplayOrdersListSerializer(order)

        return Response({
          'message': "payment status updated successfully",
          'data': response_serializer.data
        }, status=status.HTTP_200_OK)
      elif result == "failed":
        return Response({
          'error': "failed to pay"
        }, status=status.HTTP_400_BAD_REQUEST)
      else:
        return Response({
          'error': "not a valid value"
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response({
        'error': "result field is missing"
      }, status=status.HTTP_400_BAD_REQUEST)
  elif order.PaymentStatus.PAID:
    return Response({
      'error': "already paid"
    }, status=status.HTTP_400_BAD_REQUEST)