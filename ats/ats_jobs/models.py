from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()

class Tag(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()

class JobTag(Tag):
    AtsJob = models.ForeignKey('AtsJob', on_delete=models.CASCADE, related_name='ats_jobs')

class AtsJob(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    company = models.ForeignKey('companies.Company', null=True,  on_delete=models.CASCADE, related_name='ats_jobs')
    author = models.ForeignKey('users.User', null=True,  on_delete=models.CASCADE, related_name='admins')
    category = models.ForeignKey('Category', null=True,  on_delete=models.CASCADE, related_name='admins')
    tags = models.ManyToManyField(Tag)
    status = models.IntegerField(default=0);

    class Meta:
        verbose_name = "Job"

    def __str__(self):
        return "{}-{}".format(self.name, self.description)
