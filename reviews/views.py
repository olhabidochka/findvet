from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import ClinicReview, DoctorReview
from .serializers import ClinicReviewSerializer, DoctorReviewSerializer


class ClinicReviewViewSet(viewsets.ModelViewSet):
    queryset = ClinicReview.objects.filter(is_approved=True)
    serializer_class = ClinicReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['clinic', 'rating']

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return ClinicReview.objects.all()
        return ClinicReview.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoctorReviewViewSet(viewsets.ModelViewSet):
    queryset = DoctorReview.objects.filter(is_approved=True)
    serializer_class = DoctorReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'rating']

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return DoctorReview.objects.all()
        return DoctorReview.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
