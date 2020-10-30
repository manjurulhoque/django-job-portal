from django.test import TestCase
from django.urls import reverse


class TestHomeView(TestCase):
    def test_context(self):
        response = self.client.get(reverse('jobs:home'))
        self.assertGreaterEqual(len(response.context['jobs']), 0)

    def test_template_used(self):
        response = self.client.get(reverse('jobs:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
