from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):

  class Meta:
    model = CustomUser
    fields = ['id', 'username', 'password', 'first_name', 'last_name', 'fullname', 'email', 'address', 'address_type']

    extra_kwargs = {
      'password': {'write_only': True},
      'fullname': {'read_only': True}
    }
  
  def create(self, validated_data):

    user = CustomUser.objects.create_user(
      username=validated_data['username'],
      password=validated_data['password'],
      first_name=validated_data['first_name'],
      email=validated_data['email'],
      last_name=validated_data['last_name'],
      address=validated_data['address'],
      address_type=validated_data['address_type']
    )

    return user