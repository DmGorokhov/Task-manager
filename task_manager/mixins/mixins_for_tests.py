from unittest import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse_lazy


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
