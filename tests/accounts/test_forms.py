from django.test import TestCase

from accounts.forms import EmployeeRegistrationForm


class TestEmployeeRegistrationForm(TestCase):
    fixtures = ['accounts_initial_data.json']

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

    def test_employee_registration_form_valid(self):
        form = EmployeeRegistrationForm(data=self.valid_user)
        self.assertEqual(True, form.is_valid(), "Invalid form")
