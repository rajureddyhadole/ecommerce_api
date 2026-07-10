from django.urls import path
from .views import place_order, order_history, order_details, view_all_orders

urlpatterns = [
  path('orders/place/', place_order, name="place_order"),
  path('orders/', order_history, name="order_history"),
  path('orders/<int:order_id>/', order_details, name="product_details"),
  path('orders/admin/', view_all_orders, name="view_all_orders"),
]