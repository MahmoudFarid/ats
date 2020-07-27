from django.contrib import admin

from .models import Category, Job


def make_active(self, request, queryset):
    queryset.update(status=2)


make_active.short_description = "Mark selected jobs as an active"


def make_draft(self, request, queryset):
    queryset.update(status=1)


make_draft.short_description = "Mark selected jobs as a darft"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'company', 'category', 'show_description')
    list_display_links = ('company', 'category')
    list_filter = (
        ('company', admin.RelatedOnlyFieldListFilter),
        ('category', admin.RelatedOnlyFieldListFilter),
        ('status', admin.ChoicesFieldListFilter),
    )
    actions = [make_active, make_draft]
    list_select_related = ('company', 'category')
    radio_fields = {"status": admin.VERTICAL}
    sortable_by = ('id')
    list_per_page = 1

