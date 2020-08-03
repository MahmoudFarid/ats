import json

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from ats.companies.models import CompanyAdmin, CompanyStaff, Company
from ats.users.models import User
from .factories import CompanyFactory


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
        self.obj_api = '/api/companies/{}/'

        self.data = {
            "name": "test",
            "description": "Description",
            "email": "email@company.com",
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
        # #TODO: continue with checking response
        self.assertEqual(company.created_by, self.staff)
        self.assertEqual(company.website, "https://test.com")
        self.assertEqual(company.description, "Description")
        self.assertEqual(company.name, "test")

    def test_create_company_with_unauthorized_client(self):
        self.assertEqual(Company.objects.count(), 0)

        response = self.unauthorized_client.post(
            self.main_api,
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Company.objects.count(), 0)
        company = Company.objects.last()

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

    def test_create_company_with_empty_data(self):
        response = self.staff_client.post(
            self.main_api,
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        # import ipdb ; ipdb.set_trace()

    def test_create_company_with_same_data_twice(self):
        self.assertEqual(Company.objects.count(), 0)

        response = self.staff_client.post(
            self.main_api,
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(Company.objects.count(), 1)

        response = self.staff_client.post(
            self.main_api,
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_update_company_with_staff(self):
        company = CompanyFactory(created_by=self.staff)
        response = self.staff_client.put(
            self.obj_api.format(company.id),
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response.get('name'), self.data.get('name'))

    def test_update_company_with_unauthorized_client(self):
        company = CompanyFactory()
        response = self.unauthorized_client.put(
            self.obj_api.format(company.id),
            data=json.dumps(self.data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)

    def test_update_company_with_client(self):
        company = CompanyFactory()
        response = self.client.put(
            self.obj_api.format(company.id),
            data=json.dumps(self.data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)

    def test_update_another_company_information(self):
        company = CompanyFactory()
        response = self.staff_client.put(
            self.obj_api.format(company.id),
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_partial_update_company_with_staff(self):
        company = CompanyFactory(created_by=self.staff)
        response = self.staff_client.patch(
            self.obj_api.format(company.id),
            data=json.dumps({"name": "partial"}),
            content_type='application/json',
        )
        self.assertEqual(response.json().get('name'), "partial")

    def test_partial_update_company_with_unauthorized_client(self):
        company = CompanyFactory()
        response = self.unauthorized_client.patch(
            self.obj_api.format(company.id),
            data=json.dumps({"name": "partial"}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)

    def test_partial_update_company_with_client(self):
        company = CompanyFactory()
        response = self.client.patch(
            self.obj_api.format(company.id),
            data=json.dumps({"name": "partial"}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)

    def test_partial_update_another_company_information(self):
        company = CompanyFactory()
        response = self.staff_client.patch(
            self.obj_api.format(company.id),
            data=json.dumps({"name": "testing partial name"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_list_companies_with_client(self):
        CompanyFactory.create_batch(5)

        response = self.client.get(
            self.main_api
        )
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response.get('count'), 5)

    def test_list_companies_with_unauthorized_client(self):
        CompanyFactory.create_batch(3)
        response = self.unauthorized_client.get(
            self.main_api
        )
        self.assertEqual(response.json().get('count'), 3)

    def test_list_company_with_staff(self):
        CompanyFactory(created_by=self.staff)
        CompanyFactory.create_batch(3)

        response = self.staff_client.get(
            self.main_api
        )
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response.get('count'), 4)

    def test_retrieve_company_with_staff(self):
        company = CompanyFactory()
        response = self.staff_client.get(
            self.obj_api.format(company.id),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), company.id)

    def test_retrieve_company_with_unauthorized_client(self):
        company = CompanyFactory()
        response = self.staff_client.get(
            self.obj_api.format(company.id),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), company.id)
