from django.contrib import admin

from admin_log.admin import AdminLogMixin
from testproject.testapp import models


@admin.register(models.Subject)
class SubjectAdmin(AdminLogMixin, admin.ModelAdmin):
    pass
