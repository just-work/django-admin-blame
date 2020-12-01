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
