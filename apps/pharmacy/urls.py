from django.urls import path

from .views.pharmacy import (PharmacyAPIView, PharmacyDetailAPIView, 
PharmacySearchAPIView, NearbyPharmacyAPIView, 
PharmacyRegistrationView,PharmacyCountsAPIView)
from .views.medication import CategoryAPIView, MedicationDetailAPIView, MedicationAPIView, PharmacyMedicationsAPIView, PharmacyMedicationDetailAPIView, MedicationSearchAPIView
from .views.pharmacist import PharmacistDetailAPIView,PharmacistListCreateAPIView 
from .views.medication import (CategoryAPIView, MedicationDetailAPIView, MedicationAPIView, 
                               PharmacyMedicationsAPIView, PharmacyMedicationDetailAPIView,
                                 MedicationSearchAPIView, PharmacyMedicationSearchAPIView,SearchByCategoryAPIView
                                 )
from .views.subscription import SubscriptionAPIView
from .views.pharmacy import PharmacyAPIView, PharmacyDetailAPIView, PharmacySearchAPIView, NearbyPharmacyAPIView, PharmacyRegistrationView
from .views.medication import CategoryAPIView, MedicationDetailAPIView, MedicationAPIView, PharmacyMedicationsAPIView, PharmacyMedicationDetailAPIView, MedicationSearchAPIView, PharmacyMedicationSearchAPIView
from .views.subscription import SubscriptionAPIView, SubscriptionListAPIView
from .views.review import ReviewAPIView

urlpatterns = [
    path('pharmacies/', PharmacyAPIView.as_view(), name='pharmacy-list-create'),
    path('pharmacies/<int:pk>/', PharmacyDetailAPIView.as_view(), name='pharmacy-detail'),
    path('pharmacies/register/', PharmacyRegistrationView.as_view(), name='pharmacy-register'),
    path('pharmacies/search/', PharmacySearchAPIView.as_view(), name='pharmacy-search'),
    path('pharmacies/<int:pharmacy_id>/medications/', PharmacyMedicationsAPIView.as_view(), name='pharmacy-medication-list-create'),
    path('pharmacies/<int:pharmacy_id>/medications/<int:medication_id>/', PharmacyMedicationDetailAPIView.as_view(), name='pharmacy-medication-detail'),
    path('pharmacies/nearby/', NearbyPharmacyAPIView.as_view(), name='nearby-pharmacies'),
    path('pharmacies/<int:pharmacy_id>/medications/search/', PharmacyMedicationSearchAPIView.as_view(), name='pharmacy-medication-search'),
    path('pharmacy_counts/', PharmacyCountsAPIView.as_view(),name='pharmacy_counts'),
    path('pharmacies/<int:pharmacy_id>/subscribe/', SubscriptionAPIView.as_view(), name='subscribe-create-delete'),
    path('pharmacies/subscriptions/', SubscriptionListAPIView.as_view(), name='subscription-list'),
    path('pharmacies/<int:pharmacy_id>/reviews/', ReviewAPIView.as_view(), name='review-list-create'),
    
    path('medications/', MedicationAPIView.as_view(), name='medication-list-create'),
    path('medications/<int:pk>/', MedicationDetailAPIView.as_view(), name='medication-detail'),
    path('medications/search/', MedicationSearchAPIView.as_view(), name='medication-search'),
    path('categories/', CategoryAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryAPIView.as_view(), name='category-edit-delete'),

    path('pharmacists/',PharmacistListCreateAPIView.as_view(),name='pharmacist-list-create'),
    path('pharmacists/<int:pk>/', PharmacistDetailAPIView.as_view(),name='pharmacist-delete-edit'),
    path('search_by_category/<int:category_id>/', SearchByCategoryAPIView.as_view(), name='search_by_category'),
    path('search_by_category/<int:category_id>/<int:pharmacy_id>/', SearchByCategoryAPIView.as_view(), name='search_by_category_pharmacy'),

]
