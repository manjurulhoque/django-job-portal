import factory
from categories.models import Category
from faker import Faker
from django.utils.text import slugify

faker = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"{faker.word()}-{n + 1}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = faker.sentence()
