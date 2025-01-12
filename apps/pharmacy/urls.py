from django.urls import path

from .views.pharmacy import PharmacyAPIView
from .views.medication import MedicationDetailAPIView

urlpatterns = [
    path('pharmacies/', PharmacyAPIView.as_view(), name='pharmacy-list-create'),
    path('medications/<int:pk>/', MedicationDetailAPIView.as_view(), name='medication-detail'),
]
