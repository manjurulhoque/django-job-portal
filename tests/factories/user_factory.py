import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user_{n + 1}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")
