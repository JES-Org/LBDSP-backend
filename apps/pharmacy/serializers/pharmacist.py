from rest_framework import serializers

from apps.pharmacy.models.pharmacist import Pharmacist
from apps.accounts.serializers import CustomUserSerializer
from .pharmacy import PharmacySerializer
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.accounts.models import CustomUser


class PharmacistSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  
    pharmacy = PharmacySerializer(read_only=True)  
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source="user", write_only=True
    ) 
    pharmacy_id = serializers.PrimaryKeyRelatedField(
        queryset=Pharmacy.objects.all(), source="pharmacy", write_only=True
    )  

    class Meta:
        model = Pharmacist
        fields='__all__'
        read_only_fields = ['created_at']
