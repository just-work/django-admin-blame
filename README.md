Django-admin-log
==================

Django-Admin-Log is a Django app providing mixins for tracking date and author
of model changes from django admin.

[![Build Status](https://travis-ci.org/just-work/django-admin-log.svg?branch=master)](https://travis-ci.org/just-work/django-admin-log)
[![codecov](https://codecov.io/gh/just-work/django-admin-log/branch/master/graph/badge.svg)](https://codecov.io/gh/just-work/django-admin-log)
[![PyPI version](https://badge.fury.io/py/django-admin-log.svg)](https://badge.fury.io/py/django-admin-log)

Description
-----------

Often it is useful to know date and author of object creation or modification.
Django-admin-log provides a django model mixin with fields:
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
pip install django-admin-log
```

Working example is in `testproject.testapp`.

1. Enable middleware in django settings:
    ```python
    MIDDLEWARE.append('admin_log.middleware.AdminLogMiddleware')
    ```
2. Add model mixin to your models:
    ```python
    from django.contrib.auth.models import AbstractUser
    
    from admin_log.models import AdminLogMixin
    
    
    class User(AdminLogMixin, AbstractUser):
        pass
    ```
3. Add admin mixin to corresponding model admin:
    ```python
    from django.contrib import admin
    
    from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
    
    from admin_log.admin import AdminLogMixin
    from testproject.testapp import models
    
    
    @admin.register(models.User)
    class UserAdmin(AdminLogMixin, BaseUserAdmin):
        pass
    ```

Now you have readonly fields with date and author of last revision in admin
"edit" page.
