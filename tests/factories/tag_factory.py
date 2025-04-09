from factory import Faker
from factory.django import DjangoModelFactory

from tags.models import Tag


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = Faker("word")
