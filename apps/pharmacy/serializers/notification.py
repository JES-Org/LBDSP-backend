from rest_framework import serializers
from apps.pharmacy.models.notifications import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
