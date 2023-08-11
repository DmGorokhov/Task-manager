from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.users.models import SiteUser


class TestUserForms(TestCase):
    fixtures = ['db_users.json']

    @classmethod
    def setUpTestData(cls):
        cls.form_fields = ['username', 'first_name', 'last_name',
                           'password1', 'password2']

    def test_sign_up_form_fields(self):
        response = self.client.get(reverse_lazy('users:user_create'))
        form = response.context_data['form']
        self.assertEqual(len(form.fields), 5)
        for field in self.form_fields:
            self.assertIn(field, form.fields)

    def test_update_form_fields(self):
        exist_user = SiteUser.objects.get(pk=1)
        self.client.force_login(exist_user)

        response = self.client.get(
            reverse_lazy('users:user_update', kwargs={'pk': 1})
        )
        form = response.context_data['form']
        self.assertEqual(len(form.fields), 5)
        for field in self.form_fields:
            self.assertIn(field, form.fields)
