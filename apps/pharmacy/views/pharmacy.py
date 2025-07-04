from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.pharmacy.models.medication import Medication
from apps.pharmacy.serializers.pharmacy import PharmacySerializer
from apps.pharmacy.serializers.pharmacist import PharmacistSerializer
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.models.pharmacist import Pharmacist
from apps.pharmacy.signals import pharmacy_registered
from apps.pharmacy.utils.geolocation import calculate_distance

class PharmacyAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        pharmacies = Pharmacy.objects.all()
        serializer = PharmacySerializer(pharmacies, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        print("Incoming Data:", request.data)
        serializer = PharmacySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("serilizer error",serializer.errors)
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

class PharmacyRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pharmacy_data = request.data.get("pharmacy")
        pharmacist_data = request.data.get("pharmacist")

        if not pharmacy_data or not pharmacist_data:
            return Response(
                {"error": "Both pharmacy and pharmacist data are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pharmacy_serializer = PharmacySerializer(data=pharmacy_data)
        if pharmacy_serializer.is_valid():
            pharmacy = pharmacy_serializer.save()
        else:
            return Response(
                {"pharmacy_errors": pharmacy_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pharmacist_data["pharmacy_id"] = pharmacy.id
        pharmacist_data["user_id"] = request.user.id

        pharmacist_serializer = PharmacistSerializer(data=pharmacist_data)
        if pharmacist_serializer.is_valid():
            pharmacist_serializer.save(user=request.user)

            user = request.user
            if user.role != "pharmacist":
                user.role = "pharmacist"
                user.is_staff = True
                user.save()
            
            pharmacy_registered.send(sender=self.__class__, pharmacy=pharmacy)
        else:
            pharmacy.delete()
            return Response(
                {"pharmacist_errors": pharmacist_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Pharmacy registered successfully.",
                "pharmacy": pharmacy_serializer.data,
                "pharmacist": pharmacist_serializer.data["user"],
            },
            status=status.HTTP_201_CREATED,
        )

class PharmacySearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)
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

class PharmacyDashboardAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role != "pharmacist":
            return Response({"error": "youd do not have permission to access this resource"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            pharmacist = Pharmacist.objects.get(user=user)
            pharmacy = pharmacist.pharmacy

            total_medications = Medication.objects.filter(pharmacy=pharmacy).count()
            
            return Response({"total_medications": total_medications}, status=status.HTTP_200_OK)
        except Pharmacist.DoesNotExist:
            return Response({"error": "Pharmacist not found"}, status=status.HTTP_404_NOT_FOUND)
        except Pharmacy.DoesNotExist:
            return Response({"error": "Pharmacy not found"}, status=status.HTTP_404_NOT_FOUND)

class PharmacyCountsAPIView(APIView):
    def get(self, request):
        print("calling PharmacyCountsAPIView")
        total = Pharmacy.objects.count()
        pending = Pharmacy.objects.filter(status="Pending").count()
        rejected = Pharmacy.objects.filter(status="Rejected").count()
        approved = Pharmacy.objects.filter(status="Approved").count()
        return Response({
                "total": total,
                "pending": pending,
                "rejected": rejected,
                "approved": approved,
            })

