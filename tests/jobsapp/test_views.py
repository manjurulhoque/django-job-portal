from django.test import TestCase
from django.urls import reverse

from jobsapp.models import Job


class TestHomeView(TestCase):
    def test_context(self):
        response = self.client.get(reverse("jobs:home"))
        self.assertGreaterEqual(len(response.context["jobs"]), 0)

    def test_template_used(self):
        response = self.client.get(reverse("jobs:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class TestSearchView(TestCase):
    def setUp(self):
        self.url = reverse("jobs:search")
        super().setUp()

    def test_empty_query(self):
        jobs = Job.objects.filter(title__contains="software")
        response = self.client.get(self.url + "?position=software")
        self.assertFalse(b"We have found %a jobs" % str(jobs.count()) in response.content.lower())


class TestJobDetailsView(TestCase):
    def test_details(self):
        response = self.client.get(reverse("jobs:jobs-detail", args=(1,)))
        self.assertEqual(response.status_code, 404)
