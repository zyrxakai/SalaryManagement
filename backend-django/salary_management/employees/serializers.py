from rest_framework import serializers
from . models import Employee, AdminProfile
from django.contrib.auth.models import User

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'date_of_joining', 'phone_number', 'department', 'salary']

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ['id', 'name', '']