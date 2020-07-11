from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Company, CompanyAdmin

admin.site.register(Company)


@admin.register(CompanyAdmin)
class CompanyUserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'company')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'company'),
        }),
    )
    ordering = ('email',)
    list_display = ('email', 'is_staff', 'first_name', 'last_name')
    readonly_fields = ('last_login',)
