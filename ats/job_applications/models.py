from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _


class JobApplication(models.Model):
    STATUS = Choices(
        (1, 'WAITING_ACTIONS', _('Waiting Actions')),
        (2, 'SHORT_LISTED', _('Short Listed')),
        (3, 'REJECTED', _('Rejected')),
    )

    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.CASCADE, related_name="user")
    job = models.ForeignKey('jobs.Job', null=False, blank=False, on_delete=models.CASCADE, related_name="job_applications")
    status = models.IntegerField(choices=STATUS, default=STATUS.WAITING_ACTIONS)
    cv_url = models.URLField(null=True, blank=True)
    cv_file = models.FileField(upload_to='job_applications/cv/%Y/%m/%d/')

    def __str__(instance):
        return "{}-{}".format(instance.user.first_name, instance.user.last_name)
