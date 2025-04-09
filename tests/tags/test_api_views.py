from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from tests.factories.tag_factory import TagFactory


class TagListAPIViewTestCase(APITestCase):
    def setUp(self):
        TagFactory.create_batch(3)

    def test_tag_list_api_view(self):
        """Test the tag list API endpoint"""
        url = reverse("tags-api:tag-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
