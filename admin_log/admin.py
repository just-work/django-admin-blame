from django.contrib import admin


READONLY_FIELDS = ('created', 'created_by', 'modified', 'modified_by')


class AdminLogMixin:
    def get_readonly_fields(self, request, obj=None):
        """ Adds logged fields to read only fields list."""
        # noinspection PyUnresolvedReferences
        fields = super().get_readonly_fields(request, obj)
        return tuple(fields) + READONLY_FIELDS


class LoggedModelAdmin(AdminLogMixin, admin.ModelAdmin):
    """ Model admin with read-only logged fields in details view."""
