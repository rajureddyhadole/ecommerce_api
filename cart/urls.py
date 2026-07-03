from django.urls import path
from .views import  update_cart_item_quantity, cart_items_list_create

urlpatterns = [
  path('cart-items/', cart_items_list_create, name="get_cart_items"),
  path('cart-items/<int:cart_item_id>/', update_cart_item_quantity, name="update_cart_item_quantity")
]