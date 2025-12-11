from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Doctor, FavoriteDoctor
from .serializers import (DoctorListSerializer, DoctorDetailSerializer,
                          FavoriteDoctorSerializer)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.filter(is_available=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization', 'clinic']
    search_fields = ['first_name', 'last_name', 'specialization']
    ordering_fields = ['rating', 'experience_years']
    ordering = ['-rating']

    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorListSerializer
        return DoctorDetailSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_favorites(self, request, pk=None):
        doctor = self.get_object()
        favorite, created = FavoriteDoctor.objects.get_or_create(
            user=request.user,
            doctor=doctor
        )
        if created:
            return Response({'status': 'added to favorites'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already in favorites'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_from_favorites(self, request, pk=None):
        doctor = self.get_object()
        deleted = FavoriteDoctor.objects.filter(
            user=request.user,
            doctor=doctor
        ).delete()
        if deleted[0]:
            return Response({'status': 'removed from favorites'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'not in favorites'}, status=status.HTTP_404_NOT_FOUND)


class FavoriteDoctorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FavoriteDoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteDoctor.objects.filter(user=self.request.user)