from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes

from apps.pharmacy.serializers.pharmacy import PharmacySerializer
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.utils.geolocation import calculate_distance

class PharmacyAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        pharmacies = Pharmacy.objects.all()
        serializer = PharmacySerializer(pharmacies, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = PharmacySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PharmacyDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Pharmacy.objects.get(pk=pk)
        except Pharmacy.DoesNotExist:
            return None
    
    def get(self, request, pk, *args, **kwargs):
        pharmacy = self.get_object(pk)
        if not pharmacy:
            return Response({"error": "Pharmacy not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PharmacySerializer(pharmacy)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        pharmacy = self.get_object(pk=pk)
        if not pharmacy:
            return Response({"error": "Pharmacy not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PharmacySerializer(pharmacy, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        pharmacy = self.get_object(pk)
        if not pharmacy:
            return Response({"error": "Pharmacy not found"}, status=status.HTTP_404_NOT_FOUND)
        
        pharmacy.delete()

        return Response({"message": "Pharmacy deleted"}, status=status.HTTP_204_NO_CONTENT)

class PharmacySearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            pharmacies = Pharmacy.objects.filter(name__icontains=query)
        else:
            pharmacies = Pharmacy.objects.all()

        serializer = PharmacySerializer(pharmacies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NearbyPharmacyAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_lat = float(request.query_params.get('latitude', None))
        user_long = float(request.query_params.get('longitude', None))
        radius = float(request.query_params.get('radius', 5))
        if not user_lat or not user_long:
            return Response({"error": "Please provide lattitude and longitude"}, status=status.HTTP_400_BAD_REQUEST)
        
        pharmacies = Pharmacy.objects.all()
        nearby_pharmacies = []

        for pharmacy in pharmacies:
            pharmacy_lat = pharmacy.latitude
            pharmacy_long = pharmacy.longitude
            distance = calculate_distance(user_lat, user_long, pharmacy_lat, pharmacy_long)
            if distance <= radius:
                nearby_pharmacies.append(pharmacy)
        
        serializer = PharmacySerializer(nearby_pharmacies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)