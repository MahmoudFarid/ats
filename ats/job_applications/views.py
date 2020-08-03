from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import JobApplication
from .serializers import JobApplicationSerializer


class JobApplicationsViewSet(ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
