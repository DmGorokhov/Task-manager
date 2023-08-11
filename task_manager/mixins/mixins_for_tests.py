from unittest import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class MixinForTests(TestCase):

    def assert_page(self, url_pattern, template_name, response=None):
        if not response:
            response = self.client.get(reverse_lazy(url_pattern))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def assert_flashmessage(self, response, message):
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), message)

    def _check_logout_redirect_and_flash(self, response):
        error_message = _('You are logged out')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assert_flashmessage(response, error_message)

    def assert_logout_behavior(self, url_pattern, test_post_request=False,
                               data_for_post=None):
        self.client.logout()
        response = self.client.get(reverse_lazy(url_pattern))
        self._check_logout_redirect_and_flash(response)
        if test_post_request:
            response = self.client.post(reverse_lazy(url_pattern),
                                        data_for_post)
            self._check_logout_redirect_and_flash(response)
