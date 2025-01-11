from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views.pharmacy import PharmacyViewset

router = DefaultRouter()
router.register("pharmacies", PharmacyViewset)

urlpatterns = [
    path('', include(router.urls))
]
