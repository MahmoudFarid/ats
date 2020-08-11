
from rest_framework import serializers

from .models import Company
from .defaults import CompanyStaffDefault


class CompanySerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=CompanyStaffDefault())

    class Meta:
        model = Company
        fields = '__all__'

    # def validate(self, validate_data):
    #     name = validate_data.get('name')
    #     email = validate_data.get('email')
    #     errors = {}
    #     if name not in email:
    #         errors['email'] = ['Not valid email']

    #     if errors:
    #         raise serializers.ValidationError(errors)
    #     return validate_data


class ListCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'name', 'email')
