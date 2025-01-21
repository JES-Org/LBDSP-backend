from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.pharmacy.models.pharmacist import Pharmacist
from apps.pharmacy.serializers.pharmacist import PharmacistSerializer

class PharmacistListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pharmacists = Pharmacist.objects.all()
        serializer = PharmacistSerializer(pharmacists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PharmacistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
