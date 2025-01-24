from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes

from django.db.models import Q

from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.serializers.medication import CategorySerializer, MedicationSerializer
from apps.pharmacy.models.medication import Category, Medication

class MedicationAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        medications = Medication.objects.all()
        serializer = MedicationSerializer(medications, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = MedicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MedicationDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Medication.objects.get(pk=pk)
        except Medication.DoesNotExist:
            return None
    
    def get(self, request, pk, *args, **kwargs):
        medication = self.get_object(pk)
        if not medication:
            return Response({"error": "Medication not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MedicationSerializer(medication)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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

class MedicationSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get("query", None)
        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        medications = Medication.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))
        if not medications.exists():
            return Response({"message": "No medications found matching the query"}, status=status.HTTP_200_OK)

        serializer = MedicationSerializer(medications, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class PharmacyMedicationsAPIView(APIView):
    def get(self, request, pharmacy_id, *args, **kwargs):
        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)
            medications = Medication.objects.filter(pharmacy=pharmacy)
            serializer = MedicationSerializer(medications, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Pharmacy.DoesNotExist:
            return Response({"error": "pharmacy not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, pharmacy_id, *args, **kwargs):
        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)

            medication_data = request.data
            medication_data['pharmacy'] = pharmacy.id

            serializer = MedicationSerializer(data=medication_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Pharmacy.DoesNotExist:
            return Response({"error": "Pharmacy not found."}, status=status.HTTP_404_NOT_FOUND)

class PharmacyMedicationDetailAPIView(APIView):
    def get(self, request, pharmacy_id, medication_id, *args, **kwargs):
        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        except Pharmacy.DoesNotExist:
            return Response({"error": "Pharmacy not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            medication = Medication.objects.get(id=medication_id, pharmacy=pharmacy)
        except Medication.DoesNotExist:
            return Response({"error": "Medication not found in this pharmacy."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MedicationSerializer(medication)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pharmacy_id, medication_id, *args, **kwargs):
        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        except Pharmacy.DoesNotExist:
            return Response({"error": "Pharmacy not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            medication = Medication.objects.get(id=medication_id, pharmacy=pharmacy)
        except Medication.DoesNotExist:
            return Response({"error": "Medication not found in this pharmacy."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MedicationSerializer(medication, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pharmacy_id, medication_id, *args, **kwargs):
        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        except Pharmacy.DoesNotExist:
            return Response({"error": "Pharmacy not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            medication = Medication.objects.get(id=medication_id, pharmacy=pharmacy)
        except Medication.DoesNotExist:
            return Response({"error": "Medication not found in this pharmacy."}, status=status.HTTP_404_NOT_FOUND)

        medication.delete()
        return Response({"message": "Medication deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class PharmacyMedicationSearchAPIView(APIView):
    def get(self, request, pharmacy_id, *args, **kwargs):
        query = request.query_params.get("query", None)
        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        except Pharmacy.DoesNotExist:
            return Response({"error": "Pharmacy not found."}, status=status.HTTP_404_NOT_FOUND)
        
        medications = Medication.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query), pharmacy=pharmacy)
        if not medications.exists():
            return Response({"message": "No medications found matching the query"}, status=status.HTTP_200_OK)
        
        serializer = MedicationSerializer(medications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryMedicationsAPIView(APIView):
    def get(self, request, category_id, *args, **kwargs):
        medications = Medication.objects.filter(category=category_id)
        serializer = MedicationSerializer(medications, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = CategorySerializer(data=request.data, many=True)
        else:
            serializer = CategorySerializer(data=request.data)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, *args, **kwargs):
        try:
            category_id = kwargs.get('pk')  # Get the category ID from the URL
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            category_id = kwargs.get('pk')  # Get the category ID from the URL
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)    