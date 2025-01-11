from rest_framework import serializers

from ..models.pharmacy import Pharmacy

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'