from rest_framework import serializers

from ..models.medication import Medication, Category
from ..models.pharmacy import Pharmacy
from .pharmacy import PharmacySerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class MedicationSerializer(serializers.ModelSerializer):
    pharmacy_name = serializers.ReadOnlyField(source='pharmacy.name')
    category_name = serializers.ReadOnlyField(source='category.name')
    pharmacy_details = PharmacySerializer(source='pharmacy', read_only=True)
    category_details = CategorySerializer(source='category', read_only=True)
    
    class Meta:
        model = Medication
        fields = [
            'id', 
            'pharmacy', 
            'pharmacy_name', 
            'name', 
            'price', 
            'stock_status', 
            'description', 
            'category', 
            'category_name', 
            'dosage_form', 
            'dosage_strength', 
            'manufacturer', 
            'expiry_date', 
            'prescription_required', 
            'side_effects', 
            'usage_instructions', 
            'quantity_available', 
            'image',
             'pharmacy_details',  
            'category_details',
        ]
        read_only_fields = ['pharmacy_name', 'category_name', 'stock_status']
        