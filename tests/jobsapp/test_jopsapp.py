import pytest

from tests.factories import UserFactory


# Create your tests here.
@pytest.mark.django_db
class TestExample:
    def test__example__ok(self) -> None:
        user = UserFactory(first_name="Geeks", last_name=".CAT")
        assert user.first_name == "Geeks"
