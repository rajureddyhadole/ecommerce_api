from rest_framework import serializers
from .models import Order, OrderItem

class CreateOrderSerializer(serializers.ModelSerializer):

  class Meta:
    model = Order
    fields = ['shipping_address']



class DisplayOrderItemsSerializer(serializers.ModelSerializer):
  product_id = serializers.IntegerField(source='product.id', read_only=True)
  product_name = serializers.CharField(source='product.name', read_only=True)

  class Meta:
    model = OrderItem
    fields = ['product_id', 'product_name', 'quantity', 'bought_price', 'status']



class OrderDisplaySerializer(serializers.ModelSerializer):
  items = DisplayOrderItemsSerializer(many=True, read_only=True)

  class Meta:
    model = Order
    fields = ['id', 'total_amount', 'payment_status', 'shipping_address', 'created_at', 'items']


class DisplayOrdersListSerializer(serializers.ModelSerializer):

  class Meta:
    model = Order
    fields = ['id', 'total_amount', 'payment_status', 'created_at']