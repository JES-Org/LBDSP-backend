from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import CustomUserViewset

router = DefaultRouter()
router.register('users', CustomUserViewset)

urlpatterns = [
    path('', include(router.urls)),
]
