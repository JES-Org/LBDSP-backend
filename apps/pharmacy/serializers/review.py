from rest_framework import serializers

from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.models.review import Review
from apps.pharmacy.models.subscription import Subscription

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    pharmacy = serializers.PrimaryKeyRelatedField(queryset=Pharmacy.objects.all())
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'pharmacy', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']