from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Job(models.Model):
    STATUS = Choices(
        (1, 'DRAFT', _('Draft')),
        (2, 'ACTIVE', _('Active')),
        (3, 'SHORT_LISTED', _('Short Listed')),
        (4, 'REJECTED', _('Rejected')),
        (5, 'ARCHIVED', _('Archived'))
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.TextField()
    status = models.IntegerField(choices=STATUS, default=STATUS.DRAFT)
    company = models.ForeignKey('companies.Company', null=False, blank=False, on_delete=models.CASCADE, related_name='company')
    category = models.ForeignKey('Category', null=False, blank=False, on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Job"


