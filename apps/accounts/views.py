from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model

from .serializers import CustomUserSerializer

User = get_user_model()

class CustomUserViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer