from django.test import TestCase

from accounts.api.serializers import UserSerializer, UserCreateSerializer, SocialSerializer
from accounts.models import User


class TestUserSerializer(TestCase):
    def setUp(self):
        self.user_data = {"email": "test@example.com", "password": "testpass123", "role": "employee"}
        self.user = User.objects.create_user(**self.user_data)

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        self.assertEqual(serializer.data["email"], "test@example.com")
        self.assertEqual(serializer.data["role"], "employee")
        # Verify excluded fields are not in serialized data
        self.assertNotIn("password", serializer.data)
        self.assertNotIn("is_staff", serializer.data)

    def test_user_serializer_with_partial_update(self):
        update_data = {"role": "employer"}
        serializer = UserSerializer(self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.role, "employer")


class TestUserCreateSerializer(TestCase):
    def setUp(self):
        self.valid_payload = {
            "email": "newuser@example.com",
            "password": "testpass123",
            "password2": "testpass123",
            "gender": "male",
            "role": "employee",
        }

    def test_create_user_with_valid_data(self):
        serializer = UserCreateSerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.valid_payload["email"])
        self.assertEqual(user.role, self.valid_payload["role"])
        self.assertTrue(user.check_password(self.valid_payload["password"]))

    def test_create_user_with_mismatched_passwords(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["password2"] = "differentpass"
        serializer = UserCreateSerializer(data=invalid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password2", serializer.errors)

    def test_create_user_with_existing_email(self):
        # Create a user first
        User.objects.create_user(email=self.valid_payload["email"], password="somepass", role="employee")
        # Try to create another user with same email
        serializer = UserCreateSerializer(data=self.valid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
