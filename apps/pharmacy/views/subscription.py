from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.pharmacy.models.subscription import Subscription
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.serializers.subscription import SubscriptionSerializer

class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pharmacy_id = request.data.get("pharmacy")
        if not pharmacy_id:
            return Response({"error": "Pharmacy ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        except Pharmacy.DoesNotExist:
            return Response({"error": "Pharmacy not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if Subscription.objects.filter(user=request.user, pharmacy=pharmacy).exists():
            return Response({"error": "You are already subscribed to this pharmacy."}, status=status.HTTP_400_BAD_REQUEST)
        
        subscription = Subscription.objects.create(user=request.user, pharmacy=pharmacy)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        pharmacy_id = request.data.get("pharmacy")
        if not pharmacy_id:
            return Response({"error": "Pharmacy ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subscription = Subscription.objects.get(user=request.user, pharmacy_id=pharmacy_id)
            subscription.delete()
            return Response({"message": "Unsubscribed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response({"error": "You are not subscribed to this pharmacy."}, status=status.HTTP_404_NOT_FOUND)