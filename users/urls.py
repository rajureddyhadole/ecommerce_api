from django.urls import path
from .views import register, login_view
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView
)

urlpatterns = [
  path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
  path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
  path('register/', register, name="register"),
  path('login/', login_view, name="login")
]