from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from accounts.models import User


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.language_code = translation.get_language()
        self.user = User.objects.create_user(password="Abcdefgh.1", email="test@test.com")


class TestLoginView(BaseTest):
    def setUp(self) -> None:
        super(TestLoginView, self).setUp()
        self.response = self.client.get(reverse("accounts:login"))

    def test_csrf(self):
        self.assertTemplateUsed(self.response, "accounts/login.html")
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_redirect_if_authenticated(self):
        self.client.login(email="test@test.com", password="Abcdefgh.1")
        response = self.client.get(reverse("accounts:login"))
        self.assertURLEqual(reverse("jobs:home"), "/" + self.language_code + response.url)
        self.client.logout()

    def test_submit_form(self):
        response = self.client.post(reverse("accounts:login"), {"email": "test@test.com", "password": "Abcdefgh.1"})
        self.assertURLEqual(reverse("jobs:home"), "/" + self.language_code + response.url)


class TestLogoutView(BaseTest):
    def setUp(self) -> None:
        super(TestLogoutView, self).setUp()
        self.client.login(email="test@test.com", password="Abcdefgh.1")

    def test_redirect_after_logout(self):
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)
