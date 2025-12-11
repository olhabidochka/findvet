from rest_framework import serializers
from reviews.models import ClinicReview, DoctorReview


class ClinicReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)

    class Meta:
        model = ClinicReview
        fields = ['id', 'user', 'user_name', 'clinic', 'clinic_name', 'rating',
                  'comment', 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['user', 'is_approved', 'created_at', 'updated_at']


class DoctorReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)

    class Meta:
        model = DoctorReview
        fields = ['id', 'user', 'user_name', 'doctor', 'doctor_name', 'rating',
                  'comment', 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['user', 'is_approved', 'created_at', 'updated_at']