from django.db import models

from ats.users.models import User


class CompanyAdmin(User):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='admins')


class Company(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    avatar = models.ImageField(upload_to="companies", null=True, blank=True)
    email = models.EmailField(unique=True)
    website = models.URLField(unique=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return "{}-{}".format(self.name, self.description)
