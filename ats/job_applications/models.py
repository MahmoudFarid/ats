from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _


class JobApplications(models.Model):
    STATUS = Choices(
        (1, 'DRAFT', _('Draft')),
        (2, 'ACTIVE', _('Active')),
        (3, 'SHORT_LISTED', _('Short Listed')),
        (4, 'REJECTED', _('Rejected')),
        (5, 'ARCHIVED', _('Archived'))
    )

    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.CASCADE, related_name="user")
    job = models.ForeignKey('jobs.Job', null=False, blank=False, on_delete=models.CASCADE, related_name="job")
    status = models.IntegerField(choices=STATUS, default=STATUS.DRAFT)
    cv_url = models.URLField(null=True, blank=True)
    cv_file = models.FileField(upload_to='job_applications/cv/%Y/%m/%d/')

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
