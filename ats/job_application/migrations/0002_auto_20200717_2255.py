# Generated by Django 3.0.8 on 2020-07-17 22:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ats_jobs', '0006_auto_20200717_2148'),
        ('job_application', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AtsJob',
            new_name='AtsJobApplication',
        ),
    ]