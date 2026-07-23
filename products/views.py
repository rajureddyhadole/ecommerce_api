from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.


############## Product CRUD ######################

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list_create(request):
  
  if request.method == "GET":
    
    products = Product.objects.all()
    category_param = request.query_params.get('category', None)

    if category_param:

      products = products.filter(
        category=category_param
      )

    serializer = ProductSerializer(products, many=True)

    return Response({
      'data': serializer.data
    })
  

  if request.method == "POST":

    if not request.user.is_staff:

      return Response({
        'error': "You are not allowed to create product"
      }, status=status.HTTP_403_FORBIDDEN)

    serializer = ProductSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response({
      'message': "Product created successfully",
      'data': serializer.data
    }, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, product_id):

  if request.method == "GET":

    product = get_object_or_404(Product, id=product_id)

    serializer = ProductSerializer(product)

    return Response({
      'data': serializer.data
    })
  

  if request.method == "PATCH":

    if not request.user.is_staff:

      return Response({
        'error': "you are not allowed make changes"
      }, status=status.HTTP_403_FORBIDDEN)
    
    product = get_object_or_404(Product, id=product_id)

    serializer = ProductSerializer(product, data=request.data, partial=True)

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response({
      'message': "prodct edit is successfully done",
      'data': serializer.data
    })
  

  if request.method == "DELETE":

    if not request.user.is_staff:

      return Response({
        'error': "you cannot delete this."
      }, status=status.HTTP_403_FORBIDDEN)

    product = get_object_or_404(Product, id=product_id)

    product.delete()

    return Response({
      'message': "product deleted successfully",
    })


################ Category CRUD #############

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_list_create(request):

  if request.method == "GET":
    categories = Category.objects.all()

    serializer = CategorySerializer(categories, many=True)
    
    return Response({
      'message': "These are the categories",
      'data': serializer.data
    }, status=status.HTTP_200_OK)
  

  if request.method == "POST":
    
    if not request.user.is_staff:
      return Response({
        'error': "You do not have permission"
      }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CategorySerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response({
      'message': "new category created"
    }, status=status.HTTP_201_CREATED)




@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def category_detail(request, category_id):

  if request.method == "PUT":

    category = get_object_or_404(Category, id=category_id)

    serializer = CategorySerializer(category, data=request.data)

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response({
      'message': "category updated successfully"
    }, status=status.HTTP_200_OK)


  if request.method == "DELETE":

    category = get_object_or_404(Category, id=category_id)

    category.delete()

    return Response({
      'message': "category deleted successfully"
    }, status=status.HTTP_204_NO_CONTENT)
