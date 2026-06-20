from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import CreateProductSerializer, ShowProductsSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):

  category_name = request.data.get('category', None)

  if category_name:
    
    category = Category.objects.filter(name=category_name).first()

    if not category:
      category = Category.objects.create(
        name=category_name
      )
  
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


