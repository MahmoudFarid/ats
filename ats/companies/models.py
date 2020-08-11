from django.db import models

from django.utils.text import slugify

from ats.users.models import User


class CompanyAdmin(User):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='admins')


class CompanyStaff(User):
    pass


class Company(models.Model):
    created_by = models.ForeignKey('CompanyStaff', related_name='companies',
                                   on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=128)
    slug = models.SlugField(null=True)
    description = models.TextField()
    avatar = models.ImageField(upload_to="companies", null=True, blank=True)
    email = models.EmailField(unique=True)
    website = models.URLField(unique=True)
    no_employees = models.IntegerField()

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
