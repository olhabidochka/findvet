from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicReviewViewSet, DoctorReviewViewSet

router = DefaultRouter()
router.register(r'clinic-reviews', ClinicReviewViewSet, basename='clinic-review')
router.register(r'doctor-reviews', DoctorReviewViewSet, basename='doctor-review')

urlpatterns = [
    path('', include(router.urls)),
]