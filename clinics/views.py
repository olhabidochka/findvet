from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Clinic
from .serializers import ClinicListSerializer, ClinicDetailSerializer


class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city']
    search_fields = ['name', 'city', 'address']
    ordering_fields = ['rating', 'name']
    ordering = ['-rating']

    def get_serializer_class(self):
        if self.action == 'list':
            return ClinicListSerializer
        return ClinicDetailSerializer
