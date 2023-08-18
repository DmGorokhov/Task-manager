from django.test import TestCase
from task_manager.labels.models import Label
from django.db import IntegrityError


class TestLabelModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.label = Label.objects.create(name='feature')

    def test_label_creation(self):
        """Test that a label is created successfully."""
        self.assertEqual(self.label.name, 'feature')

    def test_label_string_representation(self):
        """Test that the status string representation is correct."""
        self.assertEqual(str(self.label), 'feature')

    def test_label_fields(self):
        """Test the required fields of the status model."""
        self.assertFalse(self.label._meta.get_field('name').blank)
        self.assertEqual(self.label._meta.get_field('name').null, False)

    def test_label_creation_wrong_params(self):
        with self.assertRaises(ValueError):
            Label.objects.create()

        with self.assertRaises(ValueError) as exc:
            Label.objects.create(name='')
        self.assertEqual(str(exc.exception),
                         "Label name cannot be empty string")

        with self.assertRaises(IntegrityError):
            Label.objects.create(name='same_label')
            Label.objects.create(name='same_label')
