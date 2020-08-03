
from rest_framework.routers import SimpleRouter

from .views import JobApplicationsViewSet

app_name = "job_applications"

router = SimpleRouter()

router.register('', JobApplicationsViewSet, basename='job_applications')

urlpatterns = [

] + router.urls
