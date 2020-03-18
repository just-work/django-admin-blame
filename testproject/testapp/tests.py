from admin_smoke.tests import AdminTests, AdminBaseTestCase

from testproject.testapp import admin, models


class UserAdminTestCase(AdminTests, AdminBaseTestCase):
    model_admin = admin.UserAdmin
    model = models.User
    object_name = 'user'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = models.User.objects.create_user(
            username='username',
            email='email@adminlog.com',
            password='password'
        )

    def transform_to_new(self, data: dict) -> dict:
        data['username'] += '_new'
        data['password1'] = 'unique_password'
        data['password2'] = 'unique_password'
        return data

    def test_created_by_without_admin(self):
        """ Created by is set to None if created outside of django admin."""
        self.assert_object_fields(
            self.user,
            created_by=None)

    def test_modified_by_without_admin(self):
        """ Modified by is set to None if modified outside of django admin."""
        self.user.is_active = False

        self.user.save()

        self.assert_object_fields(
            self.user,
            modified_by=None)

    def test_changeform_create(self):
        """ Created_by/modified_by for new user are set to logger user."""
        super().test_changeform_create()

        user = models.User.objects.last()
        self.assert_object_fields(
            user,
            created_by=self.superuser,
            modified_by=self.superuser)

    def test_changeform_save(self):
        """ Created_by remains untouched, modified_by is set to logged user."""
        self.update_object(
            self.user,
            created_by=self.user,
            modified_by=self.user)

        super().test_changeform_save()

        self.assert_object_fields(
            self.user,
            created_by=self.user,
            modified_by=self.superuser)
