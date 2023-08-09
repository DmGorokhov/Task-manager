from django.test import TestCase
from task_manager.users.models import SiteUser
from task_manager.utils import get_fixture_data


class SiteUserTest(TestCase):

    def setUp(self):
        self.userdata = get_fixture_data('users_data_for_tests.json', 'users')
        self.user = SiteUser.objects.create_user(**self.userdata["userdata_for_model"])

    def test_user_creation(self):
        """Test that a user is created successfully."""
        self.assertEqual(self.user.username, 'Great8')
        self.assertEqual(self.user.first_name, 'Alex')
        self.assertEqual(self.user.last_name, 'Ovechkin')
        self.assertTrue(self.user.check_password('2018'))
        self.assertFalse(self.user.is_superuser)

    def test_user_string_representation(self):
        """Test that the user string representation is correct."""
        self.assertEqual(str(self.user), 'Great8')

    def test_user_fields(self):
        """Test the required fields of the user model."""
        self.assertFalse(self.user._meta.get_field('username').blank)
        self.assertEqual(self.user._meta.get_field('username').null, False)
        self.assertFalse(self.user._meta.get_field('first_name').blank)
        self.assertEqual(self.user._meta.get_field('first_name').null, False)
        self.assertFalse(self.user._meta.get_field('last_name').blank)
        self.assertEqual(self.user._meta.get_field('last_name').null, False)

    def test_user_creation_wrong_params(self):
        with self.assertRaises(TypeError):
            SiteUser.objects.create_user()

        params_with_no_first_name = self.userdata["userdata_without_first_name"]
        with self.assertRaises(ValueError) as first_name_error:
            SiteUser.objects.create_user(params_with_no_first_name)
        self.assertEqual(str(first_name_error.exception), "The first_name and last_name must be set")

        params_with_no_last_name = self.userdata["userdata_without_last_name"]
        with self.assertRaises(ValueError):
            SiteUser.objects.create_user(params_with_no_last_name)
