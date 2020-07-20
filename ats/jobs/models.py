from django.db import models
from ats.companies.models import Company, CompanyAdmin


class Category(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Job(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 1
        ACTIVE = 2
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.TextField()
    status = models.IntegerField(Status.choices)
    company = models.ForeignKey('companies.Company', null=False, blank=False, on_delete=models.CASCADE, related_name='company')
    category = models.ForeignKey('Category', null=False, blank=False, on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Job"


