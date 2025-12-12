from rest_framework import serializers
from .models import ClinicReview, DoctorReview

class ClinicReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)

    class Meta:
        model = ClinicReview
        fields = ['id', 'clinic', 'clinic_name', 'user', 'user_name',
                  'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DoctorReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)

    class Meta:
        model = DoctorReview
        fields = ['id', 'doctor', 'doctor_name', 'user', 'user_name',
                  'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)