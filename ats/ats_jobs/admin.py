from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

# Register your models here.
from .models import AtsJob, Category, Tag

admin.site.register(AtsJob)
admin.site.register(Category)
admin.site.register(Tag)

