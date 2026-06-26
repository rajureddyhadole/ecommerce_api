from django.urls import path
from .views import create_product, show_products, edit_product, delete_product, get_product_details, create_category, edit_category, show_categories, delete_category

urlpatterns = [
  path('products/create/', create_product, name="create_product"),
  path('products/', show_products, name="show_products"),
  path("products/<int:product_id>/edit/", edit_product, name="edit_product"),
  path('products/<int:product_id>/delete/', delete_product, name="delete_product"),
  path('products/<int:product_id>/', get_product_details, name="get_product_details"),
  path('categories/', create_category, name="create_category"),
  path('categories/<int:category_id>/edit/', edit_category, name="edit_category"),
  path('categories/show/', show_categories, name="show_categories"),
  path('categories/<int:category_id>/delete/', delete_category, name="delete_category")
]