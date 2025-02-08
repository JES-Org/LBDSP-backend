from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes

from apps.pharmacy.models.review import Review
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.models.subscription import Subscription
from apps.pharmacy.serializers.review import ReviewSerializer

class ReviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pharmacy_id, *args, **kwargs):
        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        except Pharmacy.DoesNotExist:
            return Response({"error": "Pharmacy not found."}, status=status.HTTP_404_NOT_FOUND)

        reviews = Review.objects.filter(pharmacy=pharmacy)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pharmacy_id, *args, **kwargs):
        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        except Pharmacy.DoesNotExist:
            return Response({"error": "Pharmacy not found."}, status=status.HTTP_404_NOT_FOUND)

        if not Subscription.objects.filter(user=request.user, pharmacy=pharmacy).exists():
            return Response({"error": "You must be subscribed to review this pharmacy."}, status=status.HTTP_403_FORBIDDEN)

        if Review.objects.filter(user=request.user, pharmacy=pharmacy).exists():
            return Response({"error": "You have already reviewed this pharmacy."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['pharmacy'] = pharmacy_id
        serializer = ReviewSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)