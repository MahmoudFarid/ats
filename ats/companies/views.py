from django.shortcuts import render

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from rest_framework.request import Request

from rest_framework.viewsets import ModelViewSet
from .models import Company
from .serialziers import CompanySerializer


class CompaniesViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Company.objects.all()
        return queryset

    def get_serializer_class(self):
        return CompanySerializer
