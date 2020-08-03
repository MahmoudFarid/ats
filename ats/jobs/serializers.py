from rest_framework import serializers

from .models import Job
from .defaults import CompanyDefault


class JobSerializer(serializers.ModelSerializer):
    company = serializers.CharField(default=CompanyDefault())
    status = serializers.CharField(default=Job.STATUS.DRAFT)
    # status = serializers.HiddenField(initial=Job.STATUS.DRAFT, read_only=True)

    # def validate(self, validate_data):
    #     title = validate_data.get('title')
    #
    #     if not len(title):
    #         raise serializers.ValidationError()
    #     return validate_data

    class Meta:
        model = Job
        fields = '__all__'


class ListJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'title')
