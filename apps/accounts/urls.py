from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path, include

from .views import RegistrationAPIView, CustomUserAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', CustomUserAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserAPIView.as_view(), name='user-detail-delete'),
]
