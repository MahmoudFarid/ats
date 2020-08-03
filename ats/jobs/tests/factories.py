import factory.fuzzy
from faker import Faker

from ats.companies.tests.factories import CompanyFactory


from ..models import Job, Category


class CategoryFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')
    description = factory.Faker('sentence', nb_words=8)

    class Meta:
        model = Category


STATUS_ID = [status[0] for status in Job.STATUS]


class JobFactory(factory.DjangoModelFactory):
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('sentence', nb_words=8)
    tags = factory.Faker('sentence', nb_words=10)
    status = factory.fuzzy.FuzzyChoice(STATUS_ID)
    company = factory.SubFactory(CompanyFactory)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Job
