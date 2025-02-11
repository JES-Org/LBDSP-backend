from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes
from datetime import date

from django.db.models import Q
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.models.pharmacist import Pharmacist
from apps.pharmacy.models.searchHistory import SearchHistory
from apps.pharmacy.serializers.medication import CategorySerializer, MedicationSerializer
from apps.pharmacy.models.medication import Category, Medication
from django.shortcuts import get_object_or_404
from apps.pharmacy.serializers.pharmacy import PharmacySerializer
from django.utils.timezone import now
class MedicationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user=request.user
        if user.is_superuser:
            medications = Medication.objects.all()
        else:
            try:
                pharmacist=user.pharmacist_profile
                medications = Medication.objects.filter(pharmacy=pharmacist.pharmacy)
            except Pharmacist.DoesNotExist:
                 return Response(
                    {"detail": "User is not associated with a pharmacy."},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = MedicationSerializer(medications, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        user=request.user
        try:
            pharmacist=user.pharmacist_profile
        except Pharmacist.DoesNotExist:
             return Response(
                {"detail": "User is not associated with a pharmacy."},
                status=status.HTTP_403_FORBIDDEN
            )
        pharmacy=pharmacist.pharmacy
        data=request.data.copy()
        data['pharmacy'] = pharmacy.id
        serializer = MedicationSerializer(data=data)
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
        data = request.data.copy()
        data["pharmacy"] = medication.pharmacy.id
        if not medication:
            return Response({"error": "Medication not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MedicationSerializer(medication, data=data, partial=True)
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
        
        medications = Medication.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query)).select_related("pharmacy")
        if not medications.exists():
            return Response({"message": "No medications found with matching query"}, status=status.HTTP_404_NOT_FOUND)
        for medication in medications:
            search_history, created = SearchHistory.objects.get_or_create(medication=medication)
            search_history.increment_search_count()
        
         # Get distinct pharmacies from the filtered medications
        pharmacy_ids = medications.values_list("pharmacy", flat=True).distinct()
        pharmacies = Pharmacy.objects.filter(id__in=pharmacy_ids)
        if not pharmacies.exists():
            return Response({"message": "No pharmacies found with matching medications"}, status=status.HTTP_404_NOT_FOUND)

     

        serializer = PharmacySerializer(pharmacies, many=True)

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
        
        medications = Medication.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query), 
                                                pharmacy=pharmacy,stock_status=True).order_by('price')[:5]   # Sort by price and limit to 5 results
        if not medications.exists():
            return Response({"message": "No medications found matching the query"}, status=status.HTTP_200_OK)
        for medication in medications:
            search_history, created = SearchHistory.objects.get_or_create(medication=medication)
            search_history.increment_search_count()
        
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





class SearchByCategoryAPIView(APIView):
    """
    API View to search medications and pharmacies by category.
    
    - If only `category_id` is provided: Return **unique pharmacies** that sell medications in that category.
    - If `category_id` and `pharmacy_id` are provided: Return **medications** in that category from the specified pharmacy.
    """

    def get(self, request, category_id, pharmacy_id=None):
        # Validate category
        category = get_object_or_404(Category, id=category_id)
        if Category.DoesNotExist:
            return Response({"message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        

        # If a pharmacy is provided, return medications under that category for the specific pharmacy
        if pharmacy_id:
            pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
            medications = Medication.objects.filter(category=category, pharmacy=pharmacy)
            if not medications.exists():
                return Response({"message": "No medications found in this category for the specified pharmacy."}, status=status.HTTP_404_NOT_FOUND)
            for medication in medications:
                search_history, created = SearchHistory.objects.get_or_create(medication=medication)
                search_history.increment_search_count()
            

            # Serialize the medications using MedicationSerializer
            serializer = MedicationSerializer(medications, many=True)

            return Response({
                "pharmacy": PharmacySerializer(pharmacy).data,
                "medications": serializer.data
            }, status=status.HTTP_200_OK)

        # If only category_id is provided, return unique pharmacies that sell medications in this category
        medications = Medication.objects.filter(category=category).select_related('pharmacy')
        if not medications.exists():
                return Response({"message": "No medications Found"}, status=status.HTTP_404_NOT_FOUND)
        unique_pharmacies = {}

        # Serialize unique pharmacies
        for med in medications:
            search_history, created = SearchHistory.objects.get_or_create(medication=med)
            search_history.increment_search_count()
            if med.pharmacy.id not in unique_pharmacies:
                unique_pharmacies[med.pharmacy.id] = PharmacySerializer(med.pharmacy).data

        return Response(list(unique_pharmacies.values()), status=status.HTTP_200_OK)

class MedicationCountsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user=request.user
        try:
            pharmacist = user.pharmacist_profile
            medications = Medication.objects.filter(pharmacy=pharmacist.pharmacy)
        except Pharmacist.DoesNotExist:
            return Response(
                    {"detail": "User is not associated with a pharmacy."},
                    status=status.HTTP_403_FORBIDDEN
                )

          
        total = medications.count()
        inStock =medications.filter(stock_status=True).count()
        outOfStock = medications.filter(stock_status=False).count()
        expired=medications.filter(expiry_date__lt=now().date()).count()
        return Response({
                "total": total,
                "inStock": inStock,
                "outOfStock": outOfStock,
                "expired":expired,
            })
class MostSearchedMedicationsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Get the top 5 most searched medications
        most_searched = SearchHistory.get_most_searched(limit=5)

        # Prepare medication data to be returned
        medications = [entry.medication for entry in most_searched]
        serializer = MedicationSerializer(medications, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

        
class PharmacyMostSearchedMedicationsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        pharmacist = user.pharmacist_profile     
        # Fetch the most searched medications
        most_searched = SearchHistory.get_most_searched(limit=10)
        # Prepare medications and their search counts
        medications = [
            {
                'medication': entry.medication,
                'search_count': entry.search_count
            }
            for entry in most_searched
        ]
        # Filter medications based on the pharmacist's pharmacy
        filtered_medications = [
            med for med in medications if med['medication'].pharmacy == pharmacist.pharmacy
        ] 
        if not filtered_medications:
            return Response({"message": "No medications found for the most searched medications."}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicationSerializer([med['medication'] for med in filtered_medications], many=True)
        for i, data in enumerate(serializer.data):
            data['search_count'] = filtered_medications[i]['search_count']

        return Response(serializer.data, status=status.HTTP_200_OK)
class TotalMedicationsAvailableAPIView(APIView):
    def get(self, request):
        # Get the total count of medications across pharmacies
        total_medications = Medication.objects.filter(quantity_available__gt=0).count()

        # Return the result as JSON
        return Response({"total_medications": total_medications})    
class OutOfStockMedicationsAPIView(APIView):
    def get(self, request):
        out_of_stock_medications = Medication.objects.filter(quantity_available=0)
        data = out_of_stock_medications.values('name', 'category__name', 'description')

        return Response(data)
class ExpiredMedicationsAPIView(APIView):
    def get(self, request):
        expired_medications = Medication.objects.filter(expiry_date__lt=date.today())
        data = expired_medications.values('name', 'category__name', 'expiry_date', 'description')

        return Response(data)    
