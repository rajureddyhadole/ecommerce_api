from django.urls import path
from .views import place_order, order_history, order_details

urlpatterns = [
  path('orders/place/', place_order, name="place_order"),
  path('orders/', order_history, name="order_history"),
  path('orders/<int:order_id>/', order_details, name="product_details")
]