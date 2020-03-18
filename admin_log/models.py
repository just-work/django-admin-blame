from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from admin_log import fields


class AdminLogMixin(TimeStampedModel):
    """ Tracks author and date for creation and last modification."""

    created_by = fields.AutoCreatedByField(
        settings.AUTH_USER_MODEL, models.SET_NULL,
        verbose_name=_("Created by"))
    modified_by = fields.AutoModifiedByField(
        settings.AUTH_USER_MODEL, models.SET_NULL,
        verbose_name=_("Modified by"))

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        Force adding modified to update_fields if specified.

        # TODO
        This will be default behavior for TimeStampedModel in next release after
        django-model-utils==4.0.0
        """
        if update_fields is not None:
            update_fields = set(update_fields) | {'modified'}
        super().save(force_insert, force_update, using, update_fields)
