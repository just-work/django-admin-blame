from datetime import datetime
from unittest import mock

from admin_smoke.tests import AdminTests, AdminBaseTestCase
from django.contrib.auth import get_user_model
from django_testing_utils.mixins import second

from testproject.testapp import admin, models


class SubjectAdminTestCase(AdminTests, AdminBaseTestCase):
    model_admin = admin.SubjectAdmin
    model = models.Subject
    object_name = 'subject'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.subject = models.Subject.objects.create(
            title='Subject 1',
            content='Some test content.'
        )
        cls.test_user = get_user_model().objects.create(username='test_user')

    def setUp(self) -> None:
        super().setUp()
        # Django-model-utils adds django.utils.timezone.now as default to
        # AutoCreatedField. As it is done at import time, now() method
        # internally calls "datetime.now" since Django-4.0, which is C extension
        # and cannot be mocked directly. So we patch a reference to
        # datetime.datetime imported to django.utils.timezone module.
        self.model_utils_now_patcher = mock.patch(
            'django.utils.timezone.datetime.now',
            side_effect=self.get_datetime_now)
        self.model_utils_now_patcher.start()

    def tearDown(self) -> None:
        super().tearDown()
        self.model_utils_now_patcher.stop()

    def get_datetime_now(self, tz=None):
        return self.now.astimezone(tz)

    def transform_to_new(self, data: dict) -> dict:
        data['title'] += '(updated)'
        data['content'] = 'New test content.'
        return data

    def test_created_by_without_admin(self):
        """ Created by is set to None if created outside of django admin."""
        self.assert_object_fields(
            self.subject,
            created_by=None)

    def test_modified_by_without_admin(self):
        """
        Modified by is set to None if modified outside of django admin.

        Modified is still changed on save call.
        """
        self.subject.title = 'Subject 1(modified)'

        self.now += second
        self.subject.save(update_fields=['title'])

        self.assert_object_fields(
            self.subject,
            modified_by=None,
            modified=self.now)

    def test_changeform_create(self):
        """ Created_by/modified_by for new user are set to logger user."""
        super().test_changeform_create()

        subject = models.Subject.objects.last()
        self.assert_object_fields(
            subject,
            created_by=self.superuser,
            modified_by=self.superuser)

    def test_changeform_save(self):
        """ Created_by remains untouched, modified_by is set to logged user."""
        self.update_object(
            self.subject,
            created_by=self.test_user,
            modified_by=self.test_user)

        super().test_changeform_save()

        self.assert_object_fields(
            self.subject,
            created_by=self.test_user,
            modified_by=self.superuser)
