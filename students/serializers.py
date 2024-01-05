from rest_framework import serializers
from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = '__all__'

class ExtRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = ('id', 'full_name', 'email', 'phone_number', 'alternate_mobile', 'gender', 'date_of_birth', 'address', 'country', 'state', 'pincode', 'course', 'session', 'father_name', 'aadhar_number', 'created_at', 'approved')