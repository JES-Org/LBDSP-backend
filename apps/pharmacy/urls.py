from django.urls import path

from .views.pharmacy import PharmacyAPIView, PharmacyDetailAPIView
from .views.medication import CategoryAPIView, MedicationDetailAPIView, MedicationAPIView, PharmacyMedicationsAPIView, PharmacyMedicationDetailAPIView

urlpatterns = [
    path('pharmacies/', PharmacyAPIView.as_view(), name='pharmacy-list-create'),
    path('pharmacies/<int:pk>/', PharmacyDetailAPIView.as_view(), name='pharmacy-detail'),
    path('pharmacies/<int:pharmacy_id>/medications/', PharmacyMedicationsAPIView.as_view(), name='pharmacy-medication-list-create'),
    path('pharmacies/<int:pharmacy_id>/medications/<int:medication_id>/', PharmacyMedicationDetailAPIView.as_view(), name='pharmacy-medication-detail'),
    path('medications/', MedicationAPIView.as_view(), name='medication-list-create'),
    path('medications/<int:pk>/', MedicationDetailAPIView.as_view(), name='medication-detail'),
    path('categories/', CategoryAPIView.as_view(), name='category-list-create'),
]
