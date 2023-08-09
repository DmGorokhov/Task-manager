from django.urls import reverse_lazy
from task_manager.mixins.mixins_for_tests import MixinForTests
from django.test import TestCase
from django.utils.translation import gettext as _
from task_manager.users.models import SiteUser


class TestHomePage(TestCase, MixinForTests):

    def test_homepage(self):
        self.assert_page('home', 'home.html')


class Test_Login_Logout_Views(TestCase, MixinForTests):

    def test_loginpage(self):
        self.assert_page('login', 'registration/login.html')

    def test_logout_flash_and_redirect(self):
        response_logout = self.client.post(reverse_lazy('logout'))
        self.assert_flashmessage(response_logout, _('You are logged out'))
        self.assertRedirects(response_logout, reverse_lazy('home'))
