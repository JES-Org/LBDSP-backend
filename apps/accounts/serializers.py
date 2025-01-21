from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name','phone_number','last_name', 'role', 'is_staff', 'is_active', 'date_joined']
        read_only_fields = ['is_staff', 'is_active', 'date_joined']

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'phone_number','first_name', 'last_name']



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):
    print(f"Received attrs: {attrs}")
    username = attrs.get("username")
    password = attrs.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        print("Authentication failed")
        raise serializers.ValidationError(
            {"detail": "No active account found with the given credentials"}
        )
    print(f"Authenticated user: {user}")
    return super().validate(attrs)
