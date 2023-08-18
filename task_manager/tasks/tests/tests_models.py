from django.db.models import ProtectedError
from django.test import TestCase
from task_manager.tasks.models import Task
from task_manager.users.models import SiteUser
from task_manager.statuses.models import Status
from task_manager.utils import get_fixture_data
from django.db.utils import IntegrityError


class TestTaskModel(TestCase):
    fixtures = ['db_users.json', 'db_statuses.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = SiteUser.objects.get(pk=1)
        cls.user_executor = SiteUser.objects.get(pk=2)
        cls.status = Status.objects.all().first()
        cls.taskdata = get_fixture_data('tasks_data.json', 'tasks')

    def test_task_creation(self):
        """Test that a task is created successfully."""
        new_task = Task.objects.create(author=self.user, status=self.status,
                                       executor=self.user_executor,
                                       **self.taskdata['taskdata_for_model'])
        self.assertEqual(new_task.name, 'New_task')
        self.assertEqual(new_task.description, 'This is task for tests')
        self.assertEqual(new_task.author, self.user)
        self.assertEqual(new_task.executor, self.user_executor)
        self.assertEqual(new_task.labels.all().count(), 0)
        new_task.executor = None
        self.assertEqual(new_task.executor, None)
        self.assertEqual(str(new_task), 'New_task')

    def test_task_fields(self):
        new_task = Task.objects.create(author=self.user, status=self.status,
                                       executor=self.user_executor,
                                       **self.taskdata['taskdata_for_model'])
        self.assertFalse(new_task._meta.get_field('name').blank)
        self.assertTrue(new_task._meta.get_field('description').blank)
        self.assertTrue(new_task._meta.get_field('executor').blank)
        self.assertTrue(new_task._meta.get_field('executor').null)
        self.assertFalse(new_task._meta.get_field('author').blank)
        self.assertFalse(new_task._meta.get_field('author').null)
        self.assertFalse(new_task._meta.get_field('status').blank)
        self.assertFalse(new_task._meta.get_field('status').null)

    def test_empty_task(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create()

    def test_task_without_author(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(author=None, executor=self.user_executor,
                                **self.taskdata['taskdata_for_model'])

    def test_unique_task_name(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(author=self.user, executor=self.user_executor,
                                **self.taskdata['taskdata_for_model'])
            Task.objects.create(author=self.user, executor=self.user_executor,
                                **self.taskdata['taskdata_for_model'])

    def test_task_foreignkeys(self):
        new_task = Task.objects.create(author=self.user, status=self.status,  # noqa F841
                                       executor=self.user_executor,
                                       **self.taskdata['taskdata_for_model'])

        with self.assertRaises(ProtectedError):
            self.user.delete()

        with self.assertRaises(ProtectedError):
            self.status.delete()

        with self.assertRaises(ProtectedError):
            self.user_executor.delete()
