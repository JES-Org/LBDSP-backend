from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.pharmacy.models.pharmacist import Pharmacist
from apps.pharmacy.models.pharmacy import Pharmacy
from apps.accounts.models import CustomUser
from apps.pharmacy.serializers.pharmacist import PharmacistSerializer

class PharmacistListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pharmacists = Pharmacist.objects.all()
        serializer = PharmacistSerializer(pharmacists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        print("pharmacist data",data)
        user=None
        user_id = data.get("user")

        if user_id:
            user= get_object_or_404(CustomUser, id=user_id)
    

        serializer = PharmacistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user.role="pharmacist"
            user.is_staff=True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PharmacistDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pharmacist = get_object_or_404(Pharmacist, pk=pk)
        serializer = PharmacistSerializer(pharmacist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        pharmacist = get_object_or_404(Pharmacist, pk=pk)
        serializer = PharmacistSerializer(pharmacist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pharmacist = get_object_or_404(Pharmacist, pk=pk)
        pharmacist.delete()
        return Response({"detail": "Pharmacist deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
