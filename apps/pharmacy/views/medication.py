from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers.medication import MedicationSerializer
from ..models.medication import Medication

class MedicationDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Medication.objects.get(pk=pk)
        except Medication.DoesNotExist:
            return None
    
    def put(self, request, pk, *args, **kwargs):
        medication = self.get_object(pk=pk)
        if not medication:
            return Response({"error": "Medication not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MedicationSerializer(medication, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        medication = self.get_object(pk)
        if not medication:
            return Response({"error": "Medication not found"}, status=status.HTTP_404_NOT_FOUND)
        
        medication.delete()

        return Response({"message": "Medication deleted"}, status=status.HTTP_204_NO_CONTENT)