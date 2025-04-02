from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from tests.factories.category_factory import CategoryFactory
# from tests.factories.job_factory import JobFactory
# from tests.factories.user_factory import UserFactory

User = get_user_model()


class TestCommonApiViews(APITestCase):
    def setUp(self):
        # Create test data
        self.categories = CategoryFactory.create_batch(10)
        # self.jobs = JobFactory.create_batch(5)
        # self.user = UserFactory()

    def test_categories_list_api_view(self):
        """Test the categories list API endpoint"""
        url = reverse("categories:categories-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 10)

    # def test_jobs_list_api_view(self):
    #     """Test the jobs list API endpoint"""
    #     url = reverse('jobs:list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.json()), 5)

    # def test_job_detail_api_view(self):
    #     """Test the job detail API endpoint"""
    #     job = self.jobs[0]
    #     url = reverse('jobs:detail', kwargs={'slug': job.slug})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.json()['title'], job.title)

    def test_search_api_view(self):
        pass
