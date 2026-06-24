from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import CreateProductSerializer, ShowProductsSerializer, EditProductSerializer, GetProductDetailsSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.


############## Product CRUD ######################
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):

  category_name = request.data.get('category')

  if category_name:
    
    category, _ = Category.objects.get_or_create(
      name=category_name
    )
  else:
    return Response({'error': "Category is required"}, status=status.HTTP_400_BAD_REQUEST)
  
  serializer = CreateProductSerializer(data=request.data, context={'category': category})

  if serializer.is_valid():

    serializer.save()

    return Response({
      'message': "Product created successfully",
      'data': serializer.data
    }, status=status.HTTP_201_CREATED)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_products(request):

  products = Product.objects.all()

  category_param = request.query_params.get('category', None)

  if category_param:

    products = products.filter(
      category=category_param
    )

  serializer = ShowProductsSerializer(products, many=True)

  return Response({
    'data': serializer.data
  })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_details(request, product_id):
  
  product = get_object_or_404(Product, id=product_id)

  serializer = GetProductDetailsSerializer(product)

  return Response({
    'data': serializer.data
  })


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def edit_product(request, product_id):
  
  product = get_object_or_404(Product, id=product_id)

  serializer = EditProductSerializer(product, data=request.data, partial=True)

  if serializer.is_valid():

    serializer.save()

    return Response({
      'message': "prodct edit is successfully done",
      'data': serializer.data
    })
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request, product_id):
  
  product = get_object_or_404(Product, id=product_id)

  product.delete()

  return Response({
    'message': "product deleted successfully",
  })


################ Category CRUD #############
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
  
  category_name = request.data.get('category', None)

  if category_name:

    category, created = Category.objects.get_or_create(
      name=category_name
    )

    if created:

      return Response({
        'message': "category created successfully",
        'category': {
          'id': category.id,
          'name': category.name,
        }
      }, status=status.HTTP_201_CREATED)  
    else:

      return Response({
        'message': "Category already exists"
      }, status=status.HTTP_200_OK)


  return Response({
    'error': "category name not present in the request body"
  }, status=status.HTTP_400_BAD_REQUEST)