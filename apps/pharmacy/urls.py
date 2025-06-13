from django.urls import path

from .views.pharmacy import (PharmacyAPIView, PharmacyDetailAPIView, 
PharmacySearchAPIView, NearbyPharmacyAPIView, 
PharmacyRegistrationView,PharmacyCountsAPIView)
from .views.medication import CategoryAPIView, MedicationDetailAPIView, MedicationAPIView, PharmacyMedicationsAPIView, PharmacyMedicationDetailAPIView, MedicationSearchAPIView
from .views.pharmacist import PharmacistDetailAPIView,PharmacistListCreateAPIView ,PharmacistGetUpdateAPIView
from .views.medication import (CategoryAPIView, MedicationDetailAPIView, MedicationAPIView, 
                               PharmacyMedicationsAPIView, PharmacyMedicationDetailAPIView,
                                 MedicationSearchAPIView, PharmacyMedicationSearchAPIView,SearchByCategoryAPIView
                                 )
from .views.subscription import SubscriptionAPIView
from .views.pharmacy import (PharmacyAPIView, PharmacyDetailAPIView, 
                             PharmacySearchAPIView, NearbyPharmacyAPIView, 
                             PharmacyStatusReportAPIView,AllPharmacistListAPIView,
                             PharmacyRegistrationView,PharmaciesWithoutPharmacistsAPIView)
from .views.medication import (CategoryAPIView, MedicationDetailAPIView, MedicationAPIView, 
                               PharmacyMedicationsAPIView, 
                               PharmacyMedicationDetailAPIView, MedicationSearchAPIView, 
                               PharmacyMedicationSearchAPIView,MedicationCountsAPIView,
                               MostSearchedMedicationsAPIView,PharmacyMostSearchedMedicationsAPIView,BrwoseByCategoryView)
from .views.subscription import SubscriptionAPIView, SubscriptionListAPIView
from .views.review import ReviewAPIView
from .views.notification import NotificationListView,MarkNotificationAsReadView

urlpatterns = [
    path('pharmacies/', PharmacyAPIView.as_view(), name='pharmacy-list-create'),
    path('pharmacies/all/', AllPharmacistListAPIView.as_view(), name='pharmacy-list'),

    path('pharmacies-without-pharmacists/', PharmaciesWithoutPharmacistsAPIView.as_view(), name='pharmacy-without-pharmacist'),
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
    path('pharmacies/status-report/', PharmacyStatusReportAPIView.as_view(), name='pharmacy-status-report-create'),
    path('medications/', MedicationAPIView.as_view(), name='medication-list-create'),
    path('medications/<int:pk>/', MedicationDetailAPIView.as_view(), name='medication-detail'),
    path('medications/search/', MedicationSearchAPIView.as_view(), name='medication-search'),
    path('medications_counts/', MedicationCountsAPIView.as_view(),name='medications_counts'),
    path('categories/', CategoryAPIView.as_view(), name='category-list-create'),
    path('brwose_by_categories/', BrwoseByCategoryView.as_view(), name='brwose_by_categories'),
    path('categories/<int:pk>/', CategoryAPIView.as_view(), name='category-edit-delete'),
    path('pharmacists/',PharmacistListCreateAPIView.as_view(),name='pharmacist-list-create'),
    path('pharmacist/get_or_update/', PharmacistGetUpdateAPIView.as_view(), name='pharmacist-get-update'),
    path('pharmacists/<int:pk>/', PharmacistDetailAPIView.as_view(),name='pharmacist-delete-edit'),
    path('search_by_category/<int:category_id>/', SearchByCategoryAPIView.as_view(), name='search_by_category'),
    path('search_by_category/<int:category_id>/<int:pharmacy_id>/', SearchByCategoryAPIView.as_view(), name='search_by_category_pharmacy'),
    path('most-searched-medications/', MostSearchedMedicationsAPIView.as_view(), name='most-searched-medications'),
    path('pharmacy/most-searched-medications/', PharmacyMostSearchedMedicationsAPIView.as_view(), name='most-searched-medications'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/read/<int:notification_id>/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),



]
