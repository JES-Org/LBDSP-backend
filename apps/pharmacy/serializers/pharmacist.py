from rest_framework import serializers

from apps.pharmacy.models.pharmacist import Pharmacist
from apps.accounts.serializers import CustomUserSerializer

class PharmacistSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Pharmacist
        fields = ['id', 'user', 'pharmacy', 'license_number', 'license_image', 'created_at']
        read_only_fields = ['created_at']

class PharmacistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields = ['email', 'first_name', 'last_name', 'password', 'role', 'pharmacist_profile']