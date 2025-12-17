from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Clinic
from .serializers import ClinicListSerializer, ClinicDetailSerializer
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET

@require_GET
def get_google_maps_key(request):

    return JsonResponse({
        'apiKey': settings.GOOGLE_MAPS_API_KEY
    })

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
