import factory


from ats.users.tests.factories import UserFactory

from ..models import Company, CompanyStaff


class CompanyStaffFactory(UserFactory):

    class Meta:
        model = CompanyStaff


class CompanyFactory(factory.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker('sentence', nb_words=5)
    email = factory.Faker("email")
    website = factory.Sequence(lambda n: "http://comapany_%s.com" % n)
    avatar = factory.Faker('file_path')
    created_by = factory.SubFactory(CompanyStaffFactory, email=factory.SelfAttribute('..email'))
    no_employees = factory.Faker('pyint')

    class Meta:
        model = Company