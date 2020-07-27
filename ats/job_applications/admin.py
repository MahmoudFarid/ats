from django.contrib import admin

from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'user', 'status', 'cv_url')
    list_display_links = ('job', 'user', 'cv_url')
    list_filter = (
        ('user', admin.RelatedFieldListFilter),
        ('job', admin.RelatedOnlyFieldListFilter),
        'status',
    )
    sortable_by = ('id')
    list_select_related = ('user', 'job')
    list_per_page = 3

    # actions = [make_active, make_draft]
