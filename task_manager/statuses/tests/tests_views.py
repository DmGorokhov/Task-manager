from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from task_manager.statuses.models import Status
from task_manager.users.models import SiteUser
from task_manager.tasks.models import Task
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.mixins_for_tests import MixinForTests


class TestStatusCRUD(TestCase, MixinForTests):
    fixtures = ['db_users.json', 'db_statuses.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = SiteUser.objects.get(pk=1)
        cls.task = Task.objects.all().first()

    def setUp(self) -> None:
        """User should be logged in for each of CRUD operation."""
        self.client.force_login(self.user)

    def test_statuses_list(self):
        response = self.client.get(reverse_lazy('statuses:statuses_list'))
        self.assert_page('statuses:statuses_list',
                         'statuses/statuses_index.html', response)

        statuses_list = Status.objects.all().order_by('created_at')
        self.assertQuerysetEqual(
            response.context['statuses_list'],
            statuses_list)
        self.assert_logout_behavior('statuses:statuses_list')

    def test_create_status(self):
        self.assert_page('statuses:status_create',
                         'statuses/status_create.html')
        add_status = {'name': 'new_test_status'}
        response = self.client.post(reverse_lazy('statuses:status_create'),
                                    add_status)

        self.assert_flashmessage(response, _('Status is successfully created'))
        self.assertRedirects(response, reverse_lazy('statuses:statuses_list'))

        created_status = Status.objects.get(name=add_status['name'])
        self.assertEqual(created_status.__str__(), add_status['name'])

        self.assert_logout_behavior('statuses:status_create',
                                    test_post_request=True,
                                    data_for_post=add_status)

    def test_create_status_with_invalid_params(self):
        empty_status = {'name': ''}
        response = self.client.post(reverse_lazy('statuses:status_create'),
                                    empty_status)
        self.assertIn('name', response.context['form'].errors)

    def test_update_status(self):
        new_status = {'name': 'edited_status'}
        response_update_page = self.client.get(
            reverse_lazy('statuses:status_update', kwargs={'pk': 1}))
        self.assertEqual(response_update_page.status_code, 200)
        self.assertTemplateUsed(response_update_page,
                                'statuses/status_update.html')

        response = self.client.post(
            reverse_lazy('statuses:status_update', kwargs={'pk': 1}),
            new_status)
        self.assert_flashmessage(response, _('Status is successfully updated'))
        self.assertRedirects(response, reverse_lazy('statuses:statuses_list'))

        updated_status = Status.objects.get(pk=1)
        self.assertEqual(updated_status.__str__(), new_status['name'])

    def test_update_status_with_invalid_params(self):
        empty_status = {'name': ''}
        response = self.client.post(
            reverse_lazy('statuses:status_update', kwargs={'pk': 1}),
            empty_status
        )
        self.assertIn('name', response.context['form'].errors)

    def test_delete_status(self):
        exist_status = Status.objects.get(pk=1)
        response_delete_page = self.client.get(
            reverse_lazy('statuses:status_delete', kwargs={'pk': 1}))
        self.assertEqual(response_delete_page.status_code, 200)
        self.assertTemplateUsed(response_delete_page,
                                'statuses/status_delete.html')

        response = self.client.post(
            reverse_lazy('statuses:status_delete', kwargs={'pk': 1})
        )
        self.assert_flashmessage(response, _('Status is successfully deleted'))
        self.assertRedirects(response, reverse_lazy('statuses:statuses_list'))

        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(name=exist_status.name)

    def test_status_denied_changes_without_login(self):
        message = _('You are logged out')
        self.client.logout()

        response_delete_page = self.client.get(
            reverse_lazy('statuses:status_delete', kwargs={'pk': 1}))
        self.assertEqual(response_delete_page.status_code, 302)
        self.assertRedirects(response_delete_page, reverse_lazy('login'))
        self.assert_flashmessage(response_delete_page, message)

        response_update_page = self.client.get(
            reverse_lazy('statuses:status_update', kwargs={'pk': 1}))
        self.assertEqual(response_update_page.status_code, 302)
        self.assertRedirects(response_update_page, reverse_lazy('login'))
        self.assert_flashmessage(response_update_page, message)
