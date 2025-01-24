from rest_framework import serializers

from apps.pharmacy.models.pharmacist import Pharmacist
from apps.accounts.serializers import CustomUserSerializer


class PharmacistSerializer(serializers.ModelSerializer):
    pharmacy_name = serializers.ReadOnlyField(source='pharmacy.name')
    user_name = serializers.ReadOnlyField(source='user.first_name')

    class Meta:
        model = Pharmacist
        fields='__all__'
        read_only_fields = ['created_at']
        extra_fields = ['pharmacy_name',"user_name"]
