django-admin-blame
==================

django-admin-blame is a Django app providing mixins for tracking date and author
of model changes from django admin.

[![Build Status](https://github.com/just-work/django-admin-blame/workflows/build/badge.svg?branch=master&event=push)](https://github.com/just-work/django-admin-blame/actions?query=event%3Apush+branch%3Amaster+workflow%3Abuild)
[![codecov](https://codecov.io/gh/just-work/django-admin-blame/branch/master/graph/badge.svg)](https://codecov.io/gh/just-work/django-admin-blame)
[![PyPI version](https://badge.fury.io/py/django-admin-blame.svg)](https://badge.fury.io/py/django-admin-blame)

Description
-----------

Often it is useful to know date and author of object creation or modification.
django-admin-blame provides a django model mixin with fields:
* created (datetime) - timestamp of object creation
* created_by (FK to User) - reference to an admin user who created this object
    through admin site
* modified (datetime) - timestamp of last object modification
* modified_by (FK to User) - reference to an admin user who made last changes to
    this object through admin site. If changes has been made somewhere else, 
    field value is reset to `None`.

Installation
------------

```shell script
pip install django-admin-blame
```

Working example is in `testproject.testapp`.

1. Enable middleware in django settings:
    ```python
    MIDDLEWARE.append('admin_log.middleware.AdminLogMiddleware')
    ```
2. Add model mixin to your models:
    ```python
    from django.db import models
    
    from admin_log.models import AdminLogMixin
    
    
    class Subject(AdminLogMixin, models.Model):
        title = models.CharField(max_length=50)
        content = models.TextField()
    ```
3. Add admin mixin to corresponding model admin:
    ```python
    from django.contrib import admin
    
    from admin_log.admin import AdminLogMixin
    from testproject.testapp import models
    
    
    @admin.register(models.Subject)
    class SubjectAdmin(AdminLogMixin, admin.ModelAdmin):
        pass
    ```

Now you have readonly fields with date and author of last revision in admin
"edit" page.
