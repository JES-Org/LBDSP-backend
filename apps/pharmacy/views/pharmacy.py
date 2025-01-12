from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..serializers.pharmacy import PharmacySerializer
from ..models.pharmacy import Pharmacy

class PharmacyAPIView(APIView):
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