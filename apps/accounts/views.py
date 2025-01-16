from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from .serializers import RegistrationSerializer

User = get_user_model()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            user = CustomUser.objects.get(pk=pk)
            user.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user.role == 'pharmacist':
                pharmacy_id = request.data.get('pharmacy')
                if pharmacy_id:
                    from apps.pharmacy.models import Pharmacy, Pharmacist
                    pharmacy = Pharmacy.objects.get(id=pharmacy_id)
                    license_number = request.data.get('license_number')
                    license_image = request.data.get('license_image')
                    Pharmacist.objects.create(user=user, pharmacy=pharmacy, license_number=license_number, license_image=license_image)
                else:
                    return Response(
                        {"error": "Pharmacy ID is required for pharmacists."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)