from django.test import TestCase

from accounts.models import User


class TestUserModel(TestCase):
    def setUp(self) -> None:
        self.valid_user = {
            "first_name": "Manjurul",
            "last_name": "Hoque",
            "role": "employee",
            "gender": "male",
            "email": "rumi1@gmail.com",
            "password": "123456",
        }
        self.user = User.objects.create(**self.valid_user)

    def test_string_representation(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_verbose_name_plural(self):
        self.assertEqual(str(User._meta.verbose_name_plural), "users")

    def test_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Manjurul Hoque")

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email")
