from django.urls import path
from .views import add_to_cart

urlpatterns = [
  path('cart-items/', add_to_cart, name="cartitem_list_create")
]