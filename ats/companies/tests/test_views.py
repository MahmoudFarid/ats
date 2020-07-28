import json

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from ats.companies.models import CompanyAdmin, CompanyStaff, Company
from ats.users.models import User


class TestCompanyAPIViewSet(APITestCase):

    def setUp(self):
        self.staff = CompanyStaff.objects.create_user(email='admin@test.com', password='testtest')
        self.staff_client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.staff)
        self.staff_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.user = User.objects.create_user(email='user@test.com', password='testtest')
        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.unauthorized_client = APIClient()

        self.main_api = '/api/companies/'

        self.data = {
            "created_by": self.staff.id,
            "name": "Company",
            "description": "Description",
            "email": "email@email.com",
            "website": "https://test.com"
        }

    def test_create_company_with_staff(self):
        self.assertEqual(Company.objects.count(), 0)

        response = self.staff_client.post(
            self.main_api,
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Company.objects.count(), 1)
        company = Company.objects.last()
        self.assertEqual(company.created_by, self.staff)
        self.assertEqual(company.website, "https://test.com")
        self.assertEqual(company.description, "Description")
        self.assertEqual(company.name, "Company")

    def test_create_company_unauthorized_client(self):
        self.assertEqual(Company.objects.count(), 0)

        response = self.unauthorized_client.post(
            self.main_api,
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Company.objects.count(), 0)

    def test_create_company_with_client(self):
        self.assertEqual(Company.objects.count(), 0)

        response = self.client.post(
            self.main_api,
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Company.objects.count(), 0)
        company = Company.objects.last()

    def test_update_company_with_staff(self):
        response = self.staff_client.post(
            self.main_api,
            data=json.dumps(self.data),
            content_type='application/json'
        )
        company = Company.objects.last()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Company.objects.count(), 1)

        response = self.staff_client.put(
            '{}{}'.format(self.main_api, company.id),
            data={"name": "Nana"},
            format='json'
        )
        company = Company.objects.get(id=company.id)

        self.assertEqual(company.name, 'Nana')

    def test_delete_company_with_staff(self):
        response = self.staff_client.post(
            self.main_api,
            data=json.dumps(self.data),
            content_type='application/json'
        )
        company = Company.objects.last()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Company.objects.count(), 1)

        response = self.staff_client.delete(
            '{}{}'.format(self.main_api, company.id),
            content_type='application/json'
        )
        self.assertEqual(Company.objects.count(), 0)
