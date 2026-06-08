from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
  address = models.TextField()

  class Address_type(models.TextChoices):
    HOME = 'Home', 'home'
    Work = 'Work', 'work'
    OTHER = 'Other', 'other'

  address_type = models.CharField(max_length=5 , choices=Address_type.choices, default=Address_type.HOME)

  @property
  def fullname(self):
    return f"{self.first_name} {self.last_name}"
  
