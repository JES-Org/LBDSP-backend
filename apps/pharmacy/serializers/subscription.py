from rest_framework import serializers

from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.models.subscription import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    pharmacy = serializers.PrimaryKeyRelatedField(queryset=Pharmacy.objects.all())

    class Meta:
        model = Subscription
        fields = ["id", "user", "pharmacy", "subscribed_at"]
        read_only_fields = ["subscribed_at"]