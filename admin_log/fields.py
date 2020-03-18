from django.db import models
from admin_log import middleware


class AutoCreatedByField(models.ForeignKey):
    """ Automatically sets current admin user as object creator."""

    def __init__(self, to, on_delete, **kwargs):
        kwargs.setdefault('default', middleware.AdminLogMiddleware.get_user_id)
        kwargs.setdefault('related_name', '+')
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        super().__init__(to, on_delete, **kwargs)


class AutoModifiedByField(AutoCreatedByField):
    """ Automatically sets current admin user as last object change author."""

    def pre_save(self, model_instance, add):
        value = middleware.AdminLogMiddleware.get_user_id()
        setattr(model_instance, self.attname, value)
        return value
