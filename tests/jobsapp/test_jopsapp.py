import pytest

from tests.factories import UserFactory


# Create your tests here.
@pytest.mark.django_db
class TestExampe:
    def test__exemple__ok(self):
        user = UserFactory(first_name="Geeks", last_name=".CAT")
        assert user.first_name == "Geeks"
