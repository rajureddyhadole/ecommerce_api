from django.urls import path
from .views import  cart_items_list_create, cart_item_detail

urlpatterns = [
  path('cart-items/', cart_items_list_create, name="get_cart_items"),
  path('cart-items/<int:cart_item_id>/', cart_item_detail, name="cart_item_detail"),
]