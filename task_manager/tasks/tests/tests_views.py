from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from task_manager.statuses.models import Status
from task_manager.users.models import SiteUser
from task_manager.tasks.models import Task
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.mixins_for_tests import MixinForTests
from task_manager.utils import get_fixture_data


class TestTaskCRUD(TestCase, MixinForTests):
    fixtures = ['db_users.json', 'db_statuses.json', 'db_tasks']

    @classmethod
    def setUpTestData(cls):
        cls.user = SiteUser.objects.get(pk=1)
        cls.status = Status.objects.get(pk=2)
        cls.executor = SiteUser.objects.get(pk=2)
        cls.taskdata = get_fixture_data('tasks_data.json', 'tasks')

    def setUp(self) -> None:
        """User should be logged in for each of CRUD operation."""
        self.client.force_login(self.user)

    def asserTask(self, task_from_db, task_from_posted_data):
        self.assertEqual(task_from_db.__str__(), task_from_posted_data['name'])
        self.assertEqual(task_from_db.name, task_from_posted_data['name'])
        self.assertEqual(task_from_db.description,
                         task_from_posted_data['description'])
        self.assertEqual(task_from_db.author.id, self.user.id)
        self.assertEqual(task_from_db.status.id,
                         task_from_posted_data['status'])
        self.assertEqual(task_from_db.executor.id,
                         task_from_posted_data['executor'])

    def test_tasks_list(self):
        response = self.client.get(reverse_lazy('tasks:tasks_list'))
        self.assert_page('tasks:tasks_list',
                         'tasks/tasks_index.html', response)

        tasks_list = Task.objects.all().order_by('created_at')
        self.assertQuerysetEqual(
            response.context['tasks_list'],
            tasks_list)
        self.assert_logout_behavior('tasks:tasks_list')

    def test_task_detail(self):
        current_task = Task.objects.all().first()
        response_task_detail_page = self.client.get(
            reverse_lazy('tasks:task_detail', kwargs={'pk': current_task.id}))
        self.assertEqual(response_task_detail_page.status_code, 200)
        self.assertTemplateUsed(response_task_detail_page,
                                'tasks/task_detail.html')
        context = response_task_detail_page.context['task']
        self.assertEqual(context.name, current_task.name)
        self.assertEqual(context.description, current_task.description)
        self.assertEqual(context.author, current_task.author)
        self.assertEqual(context.executor, current_task.executor)
        self.assertEqual(context.status, current_task.status)
        self.assertEqual(context.created_at, current_task.created_at)

    def test_create_task(self):
        self.assert_page('tasks:task_create',
                         'tasks/task_create.html')
        new_task = {'status': self.status.id, 'executor': self.executor.id,
                    **self.taskdata["taskdata_for_model"]
                    }
        response = self.client.post(reverse_lazy('tasks:task_create'), new_task)

        self.assert_flashmessage(response, _('Task is successfully created'))
        self.assertRedirects(response, reverse_lazy('tasks:tasks_list'))

        created_task = Task.objects.get(name=new_task['name'])
        self.asserTask(created_task, new_task)

        self.assert_logout_behavior('tasks:task_create',
                                    test_post_request=True,
                                    data_for_post=new_task)

    def test_create_task_with_invalid_params(self):
        empty_task = {'name': ''}
        response = self.client.post(reverse_lazy('tasks:task_create'),
                                    empty_task)
        self.assertIn('name', response.context['form'].errors)
        task_without_status = self.taskdata["taskdata_for_model"]
        response = self.client.post(reverse_lazy('tasks:task_create'),
                                    task_without_status)
        self.assertIn('status', response.context['form'].errors)

    def test_update_task(self):
        response_update_page = self.client.get(
            reverse_lazy('tasks:task_update', kwargs={'pk': 1}))
        self.assertEqual(response_update_page.status_code, 200)
        self.assertTemplateUsed(response_update_page,
                                'tasks/task_update.html')

        taskdata_for_update = {'status': self.status.id + 1,
                               'executor': self.executor.id + 1,
                               **self.taskdata["taskdata_for_update"]
                               }
        response = self.client.post(
            reverse_lazy('tasks:task_update', kwargs={'pk': 1}),
            taskdata_for_update)
        self.assert_flashmessage(response, _('Task is successfully updated'))
        self.assertRedirects(response, reverse_lazy('tasks:tasks_list'))

        updated_task = Task.objects.get(pk=1)
        self.asserTask(updated_task, taskdata_for_update)

    def test_update_task_with_invalid_params(self):
        update_as_empty_task = {'name': ''}
        response = self.client.post(reverse_lazy('tasks:task_update',
                                                 kwargs={'pk': 1}),
                                    update_as_empty_task)
        self.assertIn('name', response.context['form'].errors)
        task_without_status = self.taskdata["taskdata_for_update"]
        response = self.client.post(reverse_lazy('tasks:task_update',
                                                 kwargs={'pk': 1}),
                                    task_without_status)
        self.assertIn('status', response.context['form'].errors)

    def test_delete_task(self):
        exist_task = Task.objects.get(pk=1)
        response_delete_page = self.client.get(
            reverse_lazy('tasks:task_delete', kwargs={'pk': 1}))
        self.assertEqual(response_delete_page.status_code, 200)
        self.assertTemplateUsed(response_delete_page,
                                'tasks/task_delete.html')

        response = self.client.post(
            reverse_lazy('tasks:task_delete', kwargs={'pk': 1})
        )
        self.assert_flashmessage(response, _('Task is successfully deleted'))
        self.assertRedirects(response, reverse_lazy('tasks:tasks_list'))

        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(name=exist_task.name)

    def test_task_denied_changes_without_login(self):
        message = _('You are logged out')
        self.client.logout()

        response_delete_page = self.client.get(
            reverse_lazy('tasks:task_delete', kwargs={'pk': 1}))
        self.assertEqual(response_delete_page.status_code, 302)
        self.assertRedirects(response_delete_page, reverse_lazy('login'))
        self.assert_flashmessage(response_delete_page, message)

        response_update_page = self.client.get(
            reverse_lazy('tasks:task_update', kwargs={'pk': 1}))
        self.assertEqual(response_update_page.status_code, 302)
        self.assertRedirects(response_update_page, reverse_lazy('login'))
        self.assert_flashmessage(response_update_page, message)

    def test_task_delete_only_author(self):
        err_message = _("A task can only be deleted by its author.")
        exist_task = Task.objects.get(pk=1)
        self.client.logout()
        another_user = SiteUser.objects.get(pk=exist_task.author.id + 1)
        self.client.force_login(another_user)

        response = self.client.post(
            reverse_lazy('tasks:task_delete', kwargs={'pk': 1})
        )

        self.assertRedirects(response, reverse_lazy('tasks:tasks_list'))
        self.assert_flashmessage(response, err_message)
