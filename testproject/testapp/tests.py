from admin_smoke.tests import AdminTests, AdminBaseTestCase
from django.contrib.auth import get_user_model

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
        """ Modified by is set to None if modified outside of django admin."""
        self.subject.title = 'Subject 1(modified)'

        self.subject.save(update_fields=['title'])

        self.assert_object_fields(
            self.subject,
            modified_by=None)

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
