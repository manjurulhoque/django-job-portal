from django.test import TestCase
from rest_framework import status
from django.urls import reverse

from tests.factories.category_factory import CategoryFactory


class TestCommonApiViews(TestCase):
    def test_categories_list_api_view(self):
        categories = CategoryFactory.create_batch(10)
        response = self.client.get(reverse("categories-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_search_api_view(self):
        pass
