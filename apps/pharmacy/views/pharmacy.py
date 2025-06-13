from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count
from apps.pharmacy.models.medication import Medication
from apps.pharmacy.serializers.pharmacy import PharmacySerializer
from apps.pharmacy.serializers.pharmacist import PharmacistSerializer
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.pharmacy.models.pharmacist import Pharmacist
from apps.pharmacy.utils.geolocation import calculate_distance
from django.db.models import Q
from apps.pharmacy.signals import pharmacy_registered
from django.core.mail import send_mail
from django.conf import settings



class AllPharmacistListAPIView(APIView):
 def get(self, request, *args, **kwargs):
        pharmacies = Pharmacy.objects.all()
        serializer = PharmacySerializer(pharmacies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

class PharmacyAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        pharmacies = Pharmacy.objects.filter(is_verified=True)
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
        if serializer.is_valid() :
            if not pharmacy.is_verified and serializer.validated_data['status'] == 'Approved':
                pharmacist=Pharmacist.objects.filter(pharmacy=pharmacy).first()
                user=pharmacist.user
                user.role = 'pharmacist'
                user.is_staff=True
                user.save()
                owner_email = user.email

                send_mail(
            "Pharmacy Registration Approved",
            f"Dear {user.first_name},\n\nYour pharmacy '{pharmacy.name}'  has been Approved.",
            settings.DEFAULT_FROM_EMAIL,
            [owner_email]
            )
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        pharmacy = self.get_object(pk)
     
        if not pharmacy:
            return Response({"error": "Pharmacy not found"}, status=status.HTTP_404_NOT_FOUND)
        pharmacist=Pharmacist.objects.filter(pharmacy=pharmacy).first()
        user=pharmacist.user
        user.role='user'
        user.is_staff=False
        user.save()
        pharmacy.delete()

        return Response({"message": "Pharmacy deleted"}, status=status.HTTP_204_NO_CONTENT)

class PharmacyRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get incoming data
        data = request.data
        # Check if the user already has a pharmacist profile
        if hasattr(request.user, 'pharmacist_profile'):
            return Response({'error': 'User already has a pharmacy.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate Pharmacy data
        pharmacy_data = {
            'name': data.get('name'),
            'address': data.get('address'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'website': data.get('website'),
            'operating_hours': data.get('operating_hours'),
            'delivery_available': data.get('delivery_available') == 'true',  # Convert to boolean
        }

        # Check if a pharmacy with the same email exists
        if Pharmacy.objects.filter(email=pharmacy_data['email']).exists():
            return Response({'error': 'A pharmacy with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create Pharmacy
        pharmacy_serializer = PharmacySerializer(data=pharmacy_data)
        if pharmacy_serializer.is_valid():
            pharmacy = pharmacy_serializer.save()  # Save the pharmacy

            # Now create the Pharmacist
            user = request.user
            # Save the user
            pharmacist_data = {
                'user_id': user.id,
                'pharmacy_id': pharmacy.id,
                'license_number': data.get('license_number'),
                'license_image': data.get('license_image'),  
            }

            # Create Pharmacist
            pharmacist_serializer = PharmacistSerializer(data=pharmacist_data)
            if pharmacist_serializer.is_valid():
                pharmacist_serializer.save()  # Save pharmacist

                # Set user role to 'pharmacist'
                

                pharmacy_registered.send(sender=self.__class__, pharmacy=pharmacy)

                return Response({
                    'pharmacy': pharmacy_serializer.data,
                    'pharmacist': pharmacist_serializer.data
                }, status=status.HTTP_201_CREATED)

            # If pharmacist data is not valid
            else:
                pharmacy.delete()
                return Response({'error': 'A pharmacy with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)


        # If pharmacy data is not valid
        return Response(pharmacy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        user_lat = request.query_params.get('latitude',None)
        user_long = request.query_params.get('longitude',None)
        lower_limit = request.query_params.get('lower_limit',None)
        upper_limit = request.query_params.get('upper_limit',None)
        # Validate latitude and longitude
        if not user_lat or not user_long:
            return Response({"error": "Please provide latitude and longitude"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_lat = float(user_lat)
            user_long = float(user_long)
        except ValueError:
            return Response({"error": "Invalid latitude or longitude format"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate limits
        if lower_limit is not None and upper_limit is not None:
            try:
                lower_limit = float(lower_limit)
                upper_limit = float(upper_limit)
            except ValueError:
                return Response({"error": "Invalid lower or upper limit format"}, status=status.HTTP_400_BAD_REQUEST)
            
            if lower_limit < 0 or upper_limit < lower_limit:
                return Response({"error": "Invalid distance range"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Default to searching for pharmacies within 5 km if no limits are provided
            lower_limit, upper_limit = 0, 5  

        pharmacies = Pharmacy.objects.all()
        filtered_pharmacies = []

        for pharmacy in pharmacies:
            pharmacy_lat = pharmacy.latitude
            pharmacy_long = pharmacy.longitude
            distance = calculate_distance(user_lat, user_long, pharmacy_lat, pharmacy_long)

            if lower_limit <= distance < upper_limit:
                filtered_pharmacies.append(pharmacy)

        serializer = PharmacySerializer(filtered_pharmacies, many=True)
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

class PharmacyStatusReportAPIView(APIView):
    def get(self, request):
        # Get total number of pharmacies
        total_count = Pharmacy.objects.count()
        # Get verified vs unverified pharmacies count
        verification_data = Pharmacy.objects.values('is_verified').annotate(total_count=Count('id'))
        
        # Convert boolean field to human-readable labels
        verification_report = [
            {"status": "Verified" if entry["is_verified"] else "Unverified", "total_count": entry["total_count"]}
            for entry in verification_data
        ]

        # Return combined response
        return Response({
            "total_pharmacies": total_count,
            "verification_report": verification_report
        }, status=status.HTTP_200_OK)
    
class PharmaciesWithoutPharmacistsAPIView(APIView):
    def get(self, request):
        # Get pharmacies that do not have an assigned pharmacist
        pharmacies_without_pharmacists = Pharmacy.objects.filter(
            ~Q(id__in=Pharmacist.objects.values_list("pharmacy_id", flat=True))
        )
        serializer = PharmacySerializer(pharmacies_without_pharmacists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
