from django.urls import path
from .views import category_list_create, category_detail, product_list_create, product_detail

urlpatterns = [
  path('products/', product_list_create, name="product_list_create"),
  path("products/<int:product_id>/", product_detail, name="product_detail"),
  path('categories/', category_list_create, name="category_list_create"),
  path('categories/<int:category_id>/', category_detail, name="category_detail"),
]