from django.contrib.auth.models import AbstractUser

from admin_log.models import AdminLogMixin


class User(AdminLogMixin, AbstractUser):
    pass
