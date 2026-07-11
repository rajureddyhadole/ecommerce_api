from rest_framework import serializers
from .models import Order, OrderItem

class CreateOrderSerializer(serializers.ModelSerializer):

  class Meta:
    model = Order
    fields = ['shipping_address']


# item details
class DisplayOrderItemsSerializer(serializers.ModelSerializer):
  product_id = serializers.IntegerField(source='product.id', read_only=True)
  product_name = serializers.CharField(source='product.name', read_only=True)

  class Meta:
    model = OrderItem
    fields = ['product_id', 'product_name', 'quantity', 'bought_price', 'status']


# order details with item details
class OrderDisplaySerializer(serializers.ModelSerializer):
  items = DisplayOrderItemsSerializer(many=True, read_only=True)

  class Meta:
    model = Order
    fields = ['id', 'total_amount', 'payment_status', 'shipping_address', 'created_at', 'items']


# order details
class DisplayOrdersListSerializer(serializers.ModelSerializer):

  class Meta:
    model = Order
    fields = ['id', 'total_amount', 'payment_status', 'created_at']


######### admin serializers ############

class ViewAllOrdersSerializer(serializers.ModelSerializer):
  customer = serializers.CharField(source="user.username", read_only=True)

  class Meta:
    model = Order
    fields = ['id', 'customer', 'total_amount', 'payment_status', 'created_at']


class ViewOrderDetailsSerializer(serializers.ModelSerializer):
  customer = serializers.CharField(source="user.username", read_only=True)
  items = DisplayOrderItemsSerializer(many=True, read_only=True)

  class Meta:
    model = Order
    fields = ['id', 'customer', 'total_amount', 'payment_status', 'created_at', 'items']
