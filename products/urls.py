from django.urls import path
from .views import create_product, show_products, edit_product

urlpatterns = [
  path('products/create/', create_product, name="create_product"),
  path('products/', show_products, name="show_products"),
  path("products/<int:product_id>/edit/", edit_product, name="edit_product")
]