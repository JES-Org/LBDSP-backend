from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from .serializers import ChangePasswordSerializer, RegistrationSerializer

User = get_user_model()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer,CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomUserAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomUserDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, *args, **kwargs):
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

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
                'user': CustomUserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetCurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk=None):
        print("logout request")
       
        try:
            user=request.user
            return Response(CustomUserSerializer(user).data) 
        except User.DoesNotExist:   
            return Response({"detail":"User not found"},status=status.HTTP_404_NOT_FOUND)   
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer          
        
class LogoutView(APIView):

    permission_classes=(IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token=request.data.get('refresh_token')
            if not refresh_token:
                return Response({'detail': 'Refresh token is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Error logging out.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
