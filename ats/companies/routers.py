
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CompaniesViewSet

app_name = "companies"

router = SimpleRouter()

router.register('', CompaniesViewSet, basename='companies')


urlpatterns = [

] + router.urls
