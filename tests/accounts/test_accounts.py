import pytest

from accounts.forms import EmployeeRegistrationForm


# Create your tests here.
@pytest.mark.django_db
class TestEmployeeRegistrationForm:
    def test__clean__ok(self):
        form = EmployeeRegistrationForm()
        form.save()
        assert form.fields["first_name"].label == "First Name"
