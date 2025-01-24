from rest_framework import serializers

from ..models.pharmacy import Pharmacy

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = [
            'id',
            'name',
            'address',
            'phone',
            'email',
            'website',
            'operating_hours',
            'is_verified',
            'image',
            'delivery_available',
            'latitude',
            'longitude',
            'status',
        ]
        read_only_fields = ['is_verified']