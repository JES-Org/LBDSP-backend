from django.urls import path

from .views.pharmacy import PharmacyAPIView, PharmacyDetailAPIView, PharmacySearchAPIView, NearbyPharmacyAPIView, PharmacyRegistrationView
from .views.medication import CategoryAPIView, MedicationDetailAPIView, MedicationAPIView, PharmacyMedicationsAPIView, PharmacyMedicationDetailAPIView, MedicationSearchAPIView, PharmacyMedicationSearchAPIView

urlpatterns = [
    path('pharmacies/', PharmacyAPIView.as_view(), name='pharmacy-list-create'),
    path('pharmacies/<int:pk>/', PharmacyDetailAPIView.as_view(), name='pharmacy-detail'),
    path('pharmacies/register/', PharmacyRegistrationView.as_view(), name='pharmacy-register'),
    path('pharmacies/search/', PharmacySearchAPIView.as_view(), name='pharmacy-search'),
    path('pharmacies/<int:pharmacy_id>/medications/', PharmacyMedicationsAPIView.as_view(), name='pharmacy-medication-list-create'),
    path('pharmacies/<int:pharmacy_id>/medications/<int:medication_id>/', PharmacyMedicationDetailAPIView.as_view(), name='pharmacy-medication-detail'),
    path('pharmacies/nearby/', NearbyPharmacyAPIView.as_view(), name='nearby-pharmacies'),
    path('pahrmacies/<int:pharmacy_id>/medications/search/', PharmacyMedicationSearchAPIView.as_view(), name='pharmacy-medication-search'),
    
    path('medications/', MedicationAPIView.as_view(), name='medication-list-create'),
    path('medications/<int:pk>/', MedicationDetailAPIView.as_view(), name='medication-detail'),
    path('medications/search/', MedicationSearchAPIView.as_view(), name='medication-search'),
    path('categories/', CategoryAPIView.as_view(), name='category-list-create'),
]
