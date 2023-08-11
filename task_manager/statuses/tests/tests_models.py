from django.test import TestCase
from task_manager.statuses.models import Status
from django.db import IntegrityError


class TestStatusModel(TestCase):

    def setUp(self):
        self.status = Status.objects.create(name='complete')

    def test_status_creation(self):
        """Test that a user is created successfully."""
        self.assertEqual(self.status.name, 'complete')

    def test_status_string_representation(self):
        """Test that the status string representation is correct."""
        self.assertEqual(str(self.status), 'complete')

    def test_status_fields(self):
        """Test the required fields of the user model."""
        self.assertFalse(self.status._meta.get_field('name').blank)
        self.assertEqual(self.status._meta.get_field('name').null, False)

    def test_status_creation_wrong_params(self):
        with self.assertRaises(ValueError):
            Status.objects.create()

        with self.assertRaises(ValueError) as exc:
            Status.objects.create(name='')
        self.assertEqual(str(exc.exception),
                         "Status name cannot be empty string")

        with self.assertRaises(IntegrityError):
            Status.objects.create(name='same_status')
            Status.objects.create(name='same_status')
