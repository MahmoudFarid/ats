from django.db import models

# Create your models here.
class AtsJobApplication(models.Model):
    job = models.ForeignKey('ats_jobs.AtsJob', null=True,  on_delete=models.CASCADE, related_name='job_application')
    user = models.ForeignKey('users.User', null=True,  on_delete=models.CASCADE, related_name='job_application')


    class Meta:
        verbose_name = "Job Application"

    def __str__(self):
        return "{}-{}".format(self.user.email, self.job.name)
