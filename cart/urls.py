from django.urls import path
from .views import add_to_cart, get_cart_items

urlpatterns = [
  # path('cart-items/', add_to_cart, name="cartitem_list_create"),
  path('cart-items/', get_cart_items, name="get_cart_items")
]