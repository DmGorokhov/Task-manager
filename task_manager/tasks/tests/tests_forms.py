from django.test import TestCase
from task_manager.tasks.forms import TaskForm
from task_manager.utils import get_fixture_data
from task_manager.statuses.models import Status
from task_manager.users.models import SiteUser


class TestTaskForm(TestCase):
    fixtures = ['db_users.json', 'db_statuses.json']

    @classmethod
    def setUpTestData(cls):
        cls.form_fields = ['name', 'description', 'status', 'executor']
        cls.user = SiteUser.objects.get(pk=1)
        cls.status = Status.objects.get(pk=2)
        cls.executor = SiteUser.objects.get(pk=2)
        cls.taskdata = get_fixture_data('tasks_data.json', 'tasks')

    def test_create_form_fields(self):
        form_data = {'status': self.status.id, 'executor': self.executor.id,
                     **self.taskdata["taskdata_for_model"]
                     }
        form = TaskForm(form_data)
        self.assertEqual(len(form.fields), 4)
        for field in self.form_fields:
            self.assertIn(field, form.fields)
        self.assertFormError(form, 'name', [])
        self.assertTrue(form.is_valid())

        invalid_form = TaskForm()
        self.assertFalse(invalid_form.is_valid())
