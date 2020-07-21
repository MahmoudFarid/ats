from django.shortcuts import render

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from rest_framework.request import Request

from rest_framework.viewsets import ModelViewSet
from .models import Company
from .serialziers import CompanySerializer
from .permissions import IsCompanyStaffPermission


class CompaniesViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyStaffPermission]

    # def get_queryset(self):
    #     queryset = Company.objects.all()
    #     return queryset

    # def get_serializer_class(self):
    #     return serializer_class
