from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

@api_view(['POST'])
def register(request):
  
  serializer = RegisterSerializer(data=request.data)

  if serializer.is_valid():

    serializer.save()

    return Response({
      'message': "user registered successfully!",
      'data': serializer.data
    }, status=status.HTTP_201_CREATED)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
  
  serializer = LoginSerializer(data=request.data)

  if serializer.is_valid():

    user = authenticate(
      username=serializer.validated_data['username'],
      password=serializer.validated_data['password']
    )

    if user is not None:

      refresh = RefreshToken.for_user(user)

      return Response({
        'message': "user logged in successfully",
        'access_token': str(refresh.access_token),
        "refresh_token": str(refresh),
        "user": {
          "id": user.id,
          'username': user.username,
          "email": user.email
        }
      }, status=status.HTTP_200_OK)
    
    return Response({'error': "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
