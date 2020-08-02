class CompanyStaffDefault:
    # https://www.django-rest-framework.org/community/3.11-announcement/#validator-default-context
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.companystaff
