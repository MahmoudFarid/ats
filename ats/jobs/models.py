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
        (2, 'ACTIVE', _('Active'))
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.TextField()
    status = models.IntegerField(choices=STATUS, default=STATUS.DRAFT)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='company')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return "{}-{}".format(self.title, self.get_status_display())
