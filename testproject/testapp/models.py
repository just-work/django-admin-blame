from django.db import models

from admin_log.models import AdminLogMixin


class Subject(AdminLogMixin, models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
