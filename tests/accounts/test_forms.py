from django.test import TestCase

from accounts.forms import EmployeeRegistrationForm, EmployerRegistrationForm
from accounts.models import User


class TestEmployeeRegistrationForm(TestCase):
    fixtures = ["accounts_initial_data.json"]

    def setUp(self) -> None:
        self.valid_user = {
            "first_name": "Manjurul",
            "last_name": "Hoque",
            "role": "employee",
            "gender": "male",
            "email": "rumi1@gmail.com",
            "password1": "123456",
            "password2": "123456",
        }

    def test_field_required(self):
        form = EmployeeRegistrationForm(data={})

        self.assertEqual(form.errors["gender"], ["Gender is required"])
        self.assertEqual(form.errors["email"], ["This field is required."])
        self.assertEqual(form.errors["password1"], ["This field is required."])
        self.assertEqual(form.errors["password2"], ["This field is required."])

    def test_employee_registration_form_valid(self):
        form = EmployeeRegistrationForm(data=self.valid_user)
        self.assertEqual(True, form.is_valid(), "Invalid form")

    def test_invalid_email(self):
        data = self.valid_user
        data["email"] = "test"
        form = EmployeeRegistrationForm(data=data)
        self.assertFalse(form.is_valid(), "Invalid email")

    def test_too_short_password(self):
        data = self.valid_user
        data["password1"] = "test"
        form = EmployeeRegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_meta_data(self):
        self.assertEqual(EmployeeRegistrationForm._meta.model, User)

        expected_fields = ["first_name", "last_name", "email", "password1", "password2", "gender"]
        for field in expected_fields:
            self.assertIn(field, EmployeeRegistrationForm._meta.fields)

    def test_password_mismatch(self):
        # Set confirm password field to a different value
        data = self.valid_user
        data["password2"] = "54321"

        form = EmployeeRegistrationForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"][0], "The two password fields didn’t match.")

    def test_valid_and_save_form(self):
        form = EmployeeRegistrationForm(data=self.valid_user)
        form.is_valid()
        user = form.save()
        self.assertIsInstance(user, User, "Not an user")


class TestEmployerRegistrationForm(TestCase):
    fixtures = ["accounts_initial_data.json"]

    def setUp(self) -> None:
        self.valid_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "employer@gmail.com",
            "password1": "123456",
            "password2": "123456",
        }

    def test_field_required(self):
        form = EmployerRegistrationForm(data={})

        self.assertEqual(form.errors["email"], ["This field is required."])
        self.assertEqual(form.errors["password1"], ["This field is required."])
        self.assertEqual(form.errors["password2"], ["This field is required."])

    def test_employee_registration_form_valid(self):
        form = EmployerRegistrationForm(data=self.valid_user)
        self.assertEqual(True, form.is_valid(), "Invalid form")

    def test_invalid_email(self):
        data = self.valid_user
        data["email"] = "test"
        form = EmployerRegistrationForm(data=data)
        self.assertFalse(form.is_valid(), "Invalid email")

    def test_too_short_password(self):
        data = self.valid_user
        data["password1"] = "test"
        form = EmployeeRegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_meta_data(self):
        self.assertEqual(EmployerRegistrationForm._meta.model, User)

        expected_fields = ["first_name", "last_name", "email", "password1", "password2"]
        for field in expected_fields:
            self.assertIn(field, EmployeeRegistrationForm._meta.fields)

    def test_password_mismatch(self):
        # Set confirm password field to a different value
        data = self.valid_user
        data["password2"] = "54321"

        form = EmployerRegistrationForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"][0], "The two password fields didn’t match.")

    def test_valid_and_save_form(self):
        form = EmployerRegistrationForm(data=self.valid_user)
        form.is_valid()
        user = form.save()
        self.assertIsInstance(user, User, "Not an user")
