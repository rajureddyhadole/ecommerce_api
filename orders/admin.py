from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'total_amount', 'shipping_address', 'payment_status', 'created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
  list_display = ['id', 'order', 'product', 'quantity', 'bought_price', 'status', 'created_at', 'updated_at']