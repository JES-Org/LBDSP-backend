from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from ..serializers.pharmacy import PharmacySerializer
from ..models.pharmacy import Pharmacy

class PharmacyViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer