from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderDisplaySerializer, DisplayOrdersListSerializer, ViewAllOrdersSerializer, ViewOrderDetailsSerializer, UpdateOrderItemStatusSerializer, PaySerializer
from .services import place_order, EmptyCartError, OutOfStock, pay_order, PayFailed, PayAlreadyDone
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order_view(request):

  serializer = CreateOrderSerializer(data=request.data)

  serializer.is_valid(raise_exception=True)

  try:
    order = place_order(
      request.user,
      serializer.validated_data['shipping_address']
    )
  except EmptyCartError as e:
    return Response({
      "error": str(e)
    }, status=status.HTTP_400_BAD_REQUEST)
  except OutOfStock as e:
    return Response({
      "error": str(e)
    }, status=status.HTTP_400_BAD_REQUEST)

  response_serializer = OrderDisplaySerializer(order)

  return Response({
    'message': "Order placed successfully",
    'data': response_serializer.data
  }, status=status.HTTP_201_CREATED)



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

  orders = Order.objects.all().select_related("user")

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

  serializer.is_valid(raise_exception=True)

  serializer.save()

  return Response({
    'message': "order Item status updated successfully",
    'data': serializer.data
  }, status=status.HTTP_200_OK)



########### payment mock ##############
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay(request, order_id):

  order = get_object_or_404(Order, id=order_id, user=request.user)

  serializer = PaySerializer(data=request.data)
  
  serializer.is_valid(raise_exception=True)

  result = serializer.validated_data['result']

  try:
    order_obj = pay_order(order, result)
  except PayFailed as e:
    return Response({
      'error': str(e)
    }, status=status.HTTP_400_BAD_REQUEST)
  except PayAlreadyDone as e:
    return Response({
      'error': str(e)
    }, status=status.HTTP_400_BAD_REQUEST)

  response_serializer = DisplayOrdersListSerializer(order_obj)
  
  return Response({
    'message': "payment status updated successfully",
    'data': response_serializer.data
  }, status=status.HTTP_200_OK)