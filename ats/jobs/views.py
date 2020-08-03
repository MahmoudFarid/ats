from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Job
from .serializers import JobSerializer
from .permissions import HasCompanyPermission, HasCompanyAdminPermission


class JobViewSet(ModelViewSet):
    permission_classes = [HasCompanyAdminPermission, HasCompanyPermission]
    protected_methods = ['POST', 'PUT', 'PATCH', 'DELETE']

    def get_queryset(self):
        if self.request.method == 'GET':
            return Job.objects.filter(status=Job.STATUS.ACTIVE)
        return Job.objects.all()

    def get_serializer_class(self):
        return JobSerializer
