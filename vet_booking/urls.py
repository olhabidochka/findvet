from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from clinics.views import ClinicViewSet
from doctors.views import DoctorViewSet, FavoriteDoctorViewSet
from services.views import ServiceViewSet
from appointments.views import AppointmentViewSet
from reviews.views import ClinicReviewViewSet, DoctorReviewViewSet
from users.views import UserRegistrationView, UserProfileView, LogoutView

router = DefaultRouter()
router.register(r'clinics', ClinicViewSet, basename='clinic')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'clinic-reviews', ClinicReviewViewSet, basename='clinic-review')
router.register(r'doctor-reviews', DoctorReviewViewSet, basename='doctor-review')
router.register(r'favorites', FavoriteDoctorViewSet, basename='favorite-doctor')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    # Authentication
    path('api/auth/register/', UserRegistrationView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/profile/', UserProfileView.as_view(), name='profile'),


    path('', include('frontend.urls')),
    path('api/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
