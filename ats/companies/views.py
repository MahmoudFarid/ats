from django.shortcuts import render

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Company
from .permissions import CompanyOwnerRequired, IsCompanyStaffPermission
from .serializers import CompanySerializer, ListCompanySerializer


class CompaniesViewSet(ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, IsCompanyStaffPermission, CompanyOwnerRequired]

    allowed_methods = ['POST', 'PUT', 'PATCH', 'DELETE']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListCompanySerializer
        return CompanySerializer
