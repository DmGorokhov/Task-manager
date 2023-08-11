from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from task_manager.users.models import SiteUser
from task_manager.utils import get_fixture_data
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.mixins_for_tests import MixinForTests


class TestUserCRUD(TestCase, MixinForTests):
    fixtures = ['db_users.json']

    def setUp(self):
        self.userdata = get_fixture_data('users_data_for_tests.json', 'users')

    def assertSiteUser(self, user_from_db, user_form_posted_data):
        self.assertEqual(user_from_db.__str__(),
                         user_form_posted_data['username'])
        self.assertEqual(user_from_db.first_name,
                         user_form_posted_data['first_name'])
        self.assertEqual(user_from_db.last_name,
                         user_form_posted_data['last_name'])

    def test_users_list(self):
        response = self.client.get(reverse_lazy('users:users_list'))
        self.assert_page('users:users_list', 'users/users_index.html', response)

        users_list = SiteUser.objects.all().order_by('date_joined')
        self.assertQuerysetEqual(
            response.context['users_list'],
            users_list
        )

    def test_create_user(self):
        self.assert_page('users:user_create', 'users/user_create.html')

        new_user = self.userdata["userdata_for_form"]
        response = self.client.post(reverse_lazy('users:user_create'), new_user)

        self.assert_flashmessage(response, _('User is successfully registered'))
        self.assertRedirects(response, reverse_lazy('login'))

        created_user = SiteUser.objects.get(username=new_user['username'])
        self.assertSiteUser(created_user, new_user)

    def test_create_user_with_validation_errors(self):
        new_user = self.userdata["userdata_for_form"]
        new_user['first_name'], new_user['last_name'] = ('', '')
        response = self.client.post(reverse_lazy('users:user_create'), new_user)
        self.assertIn('first_name', response.context['form'].errors)
        self.assertIn('last_name', response.context['form'].errors)

    def test_update_user(self):
        exist_user = SiteUser.objects.get(pk=1)
        new_user_data = self.userdata["userdata_for_update"]

        self.client.force_login(exist_user)

        response_update_page = self.client.get(
            reverse_lazy('users:user_update', kwargs={'pk': 1}))

        self.assertEqual(response_update_page.status_code, 200)
        self.assertTemplateUsed(response_update_page, 'users/user_update.html')

        response = self.client.post(
            reverse_lazy('users:user_update', kwargs={'pk': 1}),
            new_user_data,
        )
        self.assert_flashmessage(response, _('User is successfully updated'))
        self.assertRedirects(response, reverse_lazy('users:users_list'))

        updated_user = SiteUser.objects.get(pk=1)
        self.assertSiteUser(updated_user, new_user_data)

    def test_update_user_with_validation_errors(self):
        exist_user = SiteUser.objects.get(pk=1)
        new_user = self.userdata["userdata_for_form"]
        new_user['first_name'], new_user['last_name'] = ('', '')
        self.client.force_login(exist_user)

        response = self.client.post(
            reverse_lazy('users:user_update', kwargs={'pk': 1}),
            new_user,
        )
        self.assertIn('first_name', response.context['form'].errors)
        self.assertIn('last_name', response.context['form'].errors)

    def test_delete_user(self):
        exist_user = SiteUser.objects.get(pk=1)
        self.client.force_login(exist_user)
        response_update_page = self.client.get(
            reverse_lazy('users:user_delete', kwargs={'pk': 1}))

        self.assertEqual(response_update_page.status_code, 200)
        self.assertTemplateUsed(response_update_page, 'users/user_delete.html')

        response = self.client.post(reverse_lazy('users:user_delete',
                                                 kwargs={'pk': 1}))
        self.assert_flashmessage(response, _('User is successfully deleted'))
        self.assertRedirects(response, reverse_lazy('users:users_list'))

        with self.assertRaises(ObjectDoesNotExist):
            SiteUser.objects.get(username=exist_user.username)

    def test_user_denied_changes_without_login(self):
        message = _('You are logged out')

        response_delete_page = self.client.get(
            reverse_lazy('users:user_delete', kwargs={'pk': 1}))
        self.assertEqual(response_delete_page.status_code, 302)
        self.assertRedirects(response_delete_page, reverse_lazy('login'))
        self.assert_flashmessage(response_delete_page, message)

        response_update_page = self.client.get(
            reverse_lazy('users:user_update', kwargs={'pk': 1}))
        self.assertEqual(response_update_page.status_code, 302)
        self.assertRedirects(response_update_page, reverse_lazy('login'))
        self.assert_flashmessage(response_update_page, message)

    def test_denied_change_other_user(self):
        err_message = _("You have no rights to change another user.")
        exist_user = SiteUser.objects.get(pk=1)

        self.client.force_login(exist_user)
        response_update_other_user = self.client.get(
            reverse_lazy('users:user_delete', kwargs={'pk': 2}))
        self.assertRedirects(response_update_other_user,
                             reverse_lazy('users:users_list'))
        self.assert_flashmessage(response_update_other_user, err_message)

        response_delete_other_user = self.client.get(
            reverse_lazy('users:user_delete', kwargs={'pk': 2}))
        self.assertRedirects(response_delete_other_user,
                             reverse_lazy('users:users_list'))
        self.assert_flashmessage(response_delete_other_user, err_message)
