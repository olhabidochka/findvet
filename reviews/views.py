from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import ClinicReview, DoctorReview
from .serializers import ClinicReviewSerializer, DoctorReviewSerializer


class ClinicReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = ClinicReview.objects.all()


        clinic_id = self.request.query_params.get('clinic')
        if clinic_id:
            queryset = queryset.filter(clinic_id=clinic_id)


        user_filter = self.request.query_params.get('user')
        if user_filter == 'me' and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You can only edit your own reviews.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own reviews.")
        instance.delete()


class DoctorReviewViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = DoctorReview.objects.all()

        # Filter by doctor if provided
        doctor_id = self.request.query_params.get('doctor')
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        # Filter by current user
        user_filter = self.request.query_params.get('user')
        if user_filter == 'me' and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You can only edit your own reviews.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own reviews.")
        instance.delete()
