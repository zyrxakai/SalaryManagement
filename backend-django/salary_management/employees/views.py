from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Employee, AdminProfile
from . serializers import EmployeeSerializer, AdminProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

import pandas as pd

class EmployeeListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            employees = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employees)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        admin_profile = AdminProfile.objects.get(user=request.user)
        serializer = AdminProfileSerializer(admin_profile)
        return Response(serializer.data)
    
    def put(self, request):
        admin_profile = AdminProfile.objects.get(user=request.user)
        serializer = AdminProfileSerializer(admin_profile, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExcelUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES['file']
        df = pd.read_excel(file)

        for index, row in df.iterrows():
            try:
                employee = Employee.objects.get(id=row['employee_id'])
                employee.salary = row['hours_worked'] * row['rate']
                employee.save()
            except Employee.DoesNotExist:
                continue
            return Response({'message': "Salaries updated successfully"}, status=status.HTTP_200_OK)
        