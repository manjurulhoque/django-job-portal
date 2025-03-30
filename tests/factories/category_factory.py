import factory
from categories.models import Category
from faker import Faker

faker = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = faker.word()
    slug = faker.slug()
    description = faker.sentence()
