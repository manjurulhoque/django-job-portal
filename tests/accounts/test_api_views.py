from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.invalid_data = {
            "email": "invalid-email",
            "password": "short",  # too short
            "username": "test",
        }

    def setUp(self):
        self.url = reverse("accounts.api:register")
        self.valid_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "password2": "testpass123",
            "gender": "male",
            "role": "employee",
        }

    def test_registration_success(self):
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["status"])
        self.assertEqual(response.data["message"], "Successfully registered")

        # Verify user was created
        self.assertTrue(User.objects.filter(email=self.valid_data["email"]).exists())

    def test_registration_invalid_data(self):
        response = self.client.post(self.url, self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_duplicate_email(self):
        # Create a user with the same email
        User.objects.create_user(email=self.valid_data["email"], password="testpass123", role="employee")
        response = self.client.post(self.url, self.valid_data, format="json")
        """
        response
        {
            "status": False,
            "message": "A user with that email already exists. ",
            "errors": {
                "email": ["A user with that email already exists."]
            }
        }
        """
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"][0]["email"], "A user with that email already exists.")
        self.assertFalse(response.data["status"])
        self.assertEqual(response.data["message"], "A user with that email already exists. ")

    def tearDown(self):
        # Clean up created data
        User.objects.all().delete()


class EditEmployeeProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass123", role="employee")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("accounts.api:employee-profile")
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
        }

    def test_get_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["role"], self.user.role)

    def test_update_profile(self):
        response = self.client.put(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, self.valid_data["first_name"])
        self.assertEqual(self.user.last_name, self.valid_data["last_name"])
        self.assertEqual(self.user.email, self.valid_data["email"])

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
