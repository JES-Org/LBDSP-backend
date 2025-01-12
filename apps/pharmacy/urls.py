from django.urls import path

from .views.pharmacy import PharmacyAPIView

urlpatterns = [
    path('pharmacies/', PharmacyAPIView.as_view(), name='pharmacy-list-create'),
]
