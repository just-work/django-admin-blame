from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from admin_log.admin import AdminLogMixin
from testproject.testapp import models


@admin.register(models.User)
class UserAdmin(AdminLogMixin, BaseUserAdmin):
    pass
