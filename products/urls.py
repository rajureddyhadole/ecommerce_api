from django.urls import path
from .views import edit_product, delete_product, get_product_details, category_list_create, category_detail, product_list_create

urlpatterns = [
  path('products/', product_list_create, name="product_list_create"),
  path("products/<int:product_id>/edit/", edit_product, name="edit_product"),
  path('products/<int:product_id>/delete/', delete_product, name="delete_product"),
  path('products/<int:product_id>/', get_product_details, name="get_product_details"),
  path('categories/', category_list_create, name="category_list_create"),
  path('categories/<int:category_id>/', category_detail, name="category_detail"),
]