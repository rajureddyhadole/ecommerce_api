from django.urls import path
from .views import create_product, show_products

urlpatterns = [
  path('products/create/', create_product, name="create_product"),
  path('products/', show_products, name="show_products")
]