from django.urls import reverse_lazy
from task_manager.mixins.mixins_for_tests import MixinForTests
from django.test import TestCase
from django.utils.translation import gettext as _
from task_manager.users.models import SiteUser


class TestHomePage(TestCase, MixinForTests):
    fixtures = ['db_users.json']

    def setUp(self) -> None:
        self.login_navbar_fields = [_('Statuses'),
                                    _('Labels'),
                                    _('Tasks'),
                                    _('Logout')
                                    ]
        self.logout_navbar_fields = [_('Login'),
                                     _('Sign Up'),
                                     ]

    def test_homepage(self):
        self.assert_page('home', 'home.html')

    def test_homepage_without_login(self):
        response = self.client.get(reverse_lazy('home'))
        for field in self.login_navbar_fields:
            self.assertNotContains(response, field)

        for field in self.logout_navbar_fields:
            self.assertContains(response, field)

    def test_homepage_with_login(self):
        user = SiteUser.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('home'))
        for field in self.login_navbar_fields:
            self.assertContains(response, field)

        for field in self.logout_navbar_fields:
            self.assertNotContains(response, field)


class Test_Login_Logout_Views(TestCase, MixinForTests):

    def test_loginpage(self):
        self.assert_page('login', 'registration/login.html')

    def test_logout_flash_and_redirect(self):
        response_logout = self.client.post(reverse_lazy('logout'))
        self.assert_flashmessage(response_logout, _('You are logged out'))
        self.assertRedirects(response_logout, reverse_lazy('home'))
