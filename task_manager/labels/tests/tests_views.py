from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from task_manager.labels.models import Label
from task_manager.users.models import SiteUser
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.mixins_for_tests import MixinForTests


class TestLabelCRUD(TestCase, MixinForTests):
    fixtures = ['db_users.json', 'db_labels.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = SiteUser.objects.get(pk=1)

    def setUp(self) -> None:
        """User should be logged in for each of CRUD operation."""
        self.client.force_login(self.user)

    def test_labels_list(self):
        response = self.client.get(reverse_lazy('labels:labels_list'))
        self.assert_page('labels:labels_list',
                         'labels/labels_index.html', response)

        labels_list = Label.objects.all().order_by('created_at')
        self.assertQuerysetEqual(
            response.context['labels_list'],
            labels_list)
        self.assert_logout_behavior('labels:labels_list')

    def test_create_label(self):
        self.assert_page('labels:label_create',
                         'labels/label_create.html')
        add_label = {'name': 'new_test_label'}
        response = self.client.post(reverse_lazy('labels:label_create'),
                                    add_label)

        self.assert_flashmessage(response, _('Label is successfully created'))
        self.assertRedirects(response, reverse_lazy('labels:labels_list'))

        created_label = Label.objects.get(name=add_label['name'])
        self.assertEqual(created_label.__str__(), add_label['name'])

        self.assert_logout_behavior('labels:label_create',
                                    test_post_request=True,
                                    data_for_post=add_label)

    def test_create_label_with_invalid_params(self):
        empty_label = {'name': ''}
        response = self.client.post(reverse_lazy('labels:label_create'),
                                    empty_label)
        self.assertIn('name', response.context['form'].errors)

    def test_update_label(self):
        new_label = {'name': 'edited_label'}
        response_update_page = self.client.get(
            reverse_lazy('labels:label_update', kwargs={'pk': 1}))
        self.assertEqual(response_update_page.status_code, 200)
        self.assertTemplateUsed(response_update_page,
                                'labels/label_update.html')

        response = self.client.post(
            reverse_lazy('labels:label_update', kwargs={'pk': 1}),
            new_label)
        self.assert_flashmessage(response, _('Label is successfully updated'))
        self.assertRedirects(response, reverse_lazy('labels:labels_list'))

        updated_status = Label.objects.get(pk=1)
        self.assertEqual(updated_status.__str__(), new_label['name'])

    def test_update_label_with_invalid_params(self):
        empty_label = {'name': ''}
        response = self.client.post(
            reverse_lazy('labels:label_update', kwargs={'pk': 1}),
            empty_label
        )
        self.assertIn('name', response.context['form'].errors)

    def test_delete_label(self):
        exist_label = Label.objects.get(pk=1)
        response_delete_page = self.client.get(
            reverse_lazy('labels:label_delete', kwargs={'pk': 1}))
        self.assertEqual(response_delete_page.status_code, 200)
        self.assertTemplateUsed(response_delete_page,
                                'labels/label_delete.html')

        response = self.client.post(
            reverse_lazy('labels:label_delete', kwargs={'pk': 1})
        )
        self.assert_flashmessage(response, _('Label is successfully deleted'))
        self.assertRedirects(response, reverse_lazy('labels:labels_list'))

        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(name=exist_label.name)

    def test_label_denied_changes_without_login(self):
        message = _('You are logged out')
        self.client.logout()

        response_delete_page = self.client.get(
            reverse_lazy('labels:label_delete', kwargs={'pk': 1}))
        self.assertEqual(response_delete_page.status_code, 302)
        self.assertRedirects(response_delete_page, reverse_lazy('login'))
        self.assert_flashmessage(response_delete_page, message)

        response_update_page = self.client.get(
            reverse_lazy('labels:label_update', kwargs={'pk': 1}))
        self.assertEqual(response_update_page.status_code, 302)
        self.assertRedirects(response_update_page, reverse_lazy('login'))
        self.assert_flashmessage(response_update_page, message)
