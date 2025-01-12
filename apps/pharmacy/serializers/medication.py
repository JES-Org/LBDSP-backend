from rest_framework import serializers

from ..models.medication import Medication, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class MedicationSerializer(serializers.ModelSerializer):
    pharmacy_name = serializers.ReadOnlyField(source='pharmacy.name')
    category_name = serializers.ReadOnlyField(source='category.name')

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
        ]
        read_only_fields = ['pharmacy_name', 'category_name', 'stock_status']
        