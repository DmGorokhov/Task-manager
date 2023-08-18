from django.test import TestCase
from task_manager.labels.forms import LabelForm


class TestLabelForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form_fields = ['name']

    def test_create_form_fields(self):
        form_data = {'name': 'Test label'}
        form = LabelForm(form_data)
        self.assertEqual(len(form.fields), 1)
        for field in self.form_fields:
            self.assertIn(field, form.fields)
        self.assertFormError(form, 'name', [])
        self.assertTrue(form.is_valid())

        invalid_form = LabelForm()
        self.assertFalse(invalid_form.is_valid())
