from rest_framework.routers import SimpleRouter

from .views import JobViewSet


app_name = "jobs"

router = SimpleRouter()
router.register('', JobViewSet, basename='jobs')

urlpatterns = [

] + router.urls
