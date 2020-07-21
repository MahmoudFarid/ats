
from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'

    def validate(self, attrs):
        return attrs
