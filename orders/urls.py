from django.urls import path
from .views import place_order_view, order_history, order_details, view_all_orders, view_order_details, update_order_item_status, pay

urlpatterns = [
  path('orders/place/', place_order_view, name="place_order"),
  path('orders/', order_history, name="order_history"),
  path('orders/<int:order_id>/', order_details, name="product_details"),
  path('orders/admin/', view_all_orders, name="view_all_orders"),
  path('orders/<int:order_id>/admin/', view_order_details, name="view_order_details"),
  path('order-items/<int:order_item_id>/admin/', update_order_item_status, name="update_order_item_status"),
  path('orders/<int:order_id>/pay/', pay, name="payment")
]